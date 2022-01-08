import datetime
from flask import request, jsonify
from flask_login import login_user, current_user
from sqlalchemy import desc

from messaging_api.models import User, Message
from messaging_api import app, message_validator, login_validator, db
from flask_bcrypt import Bcrypt


# Route to write a message
@app.route('/message', methods=['POST'])
def message():
    req_data = request.get_json()
    # Check form validation
    if message_validator.validate(req_data):
        # Check if current user logged in is indeed the sender
        if current_user.is_authenticated and current_user.username == req_data['sender']:
            # Check if receiver user exists in DB.
            _receiver = User.query.filter_by(username=req_data['receiver']).first()
            if _receiver:

                msg = Message(
                    sender=req_data['sender'],
                    receiver=req_data['receiver'],
                    message=req_data['message'],
                    subject=req_data['subject']
                )
                db.session.add(msg)
                db.session.commit()
                return {'message': f"Message sent to {req_data['receiver']}"}, 200
            else:
                # Receiver does not exist
                return {'message': f"User {req_data['receiver']} does not exist."}, 401
        else:
            return {'message': 'You need to be logged in to do that.'}, 401

    else:
        return message_validator.errors, 400


# Route to get all messages that the current logged in user received / sent.
@app.route('/get_messages')
def get_messages():
    if current_user.is_authenticated:

        sent_msgs = [Message.as_dict(msg) for msg in current_user.messages_sent]
        rec_msgs = [Message.as_dict(msg) for msg in current_user.messages_received]

        # Change status of all messages to True.  -  Not sure if I should do this.
        # for msg in Message.query.filter_by(receiver=current_user.username).all():
        #     msg.read = True
        # Commit changes to the server.
        db.session.commit()
        # Make messages dict.
        msgs_dict = {'sent_messages': sent_msgs, 'received_messages': rec_msgs}
        return jsonify(msgs_dict), 200
    else:
        return {'message': 'You need to be logged in'}, 400


# Route to get all unread messages the current user logged in has received.
@app.route('/get_unread')
def get_unread():
    if current_user.is_authenticated:
        # get a list of all unread messages that the current user received.
        unread = list(filter((lambda msg: msg.read is False), current_user.messages_received))
        # turn each message to a dictionary.
        unread = [Message.as_dict(msg) for msg in unread]
        return jsonify(unread), 200
    else:
        return {'message': 'You need to be logged in for that.'}, 401


# Route to get the last unread message sent to the currently logged in user.
@app.route('/read_message')
def read_message():
    return_msg = None
    if current_user.is_authenticated:
        # Get the last ( by id ) unread message the current user received. Sorry for the long line.
        msg = Message.query.filter_by(read=False, receiver=current_user.username).order_by(desc(Message.id)).first()
        if msg:
            return_msg = Message.as_dict(msg)
            msg.read = True
        db.session.commit()
        return return_msg or {'message': 'No unread messages.'}, 200
    else:
        return {'message': 'You need to be logged in for that.'}, 401


# Route to delete a message by id. This route does not make use of any request-body.
@app.route('/delete/<req_id>', methods=['DELETE'])
def delete_message(req_id):

    msg = Message.query.filter_by(id=req_id).first()
    if msg and msg.sender == current_user.username:
        db.session.delete(msg)
        db.session.commit()
        return {'message': 'message was deleted.'}, 200
    elif msg:
        # Message sender is not current user.
        return {'message': 'You are not authorized.'}, 403
    else:
        return {'message': "Message does not exist."}, 400


# Route to log in based on existing users currently in the database.
@app.route('/login')
def login():
    req_data = request.get_json()
    # Form validated.
    if login_validator.validate(req_data):
        # Get the user by username sent in the request-body
        _user = User.query.filter_by(username=req_data['username']).first()
        # User must exist in DB, and passwords must match.
        if _user and Bcrypt().check_password_hash(_user.password, req_data['password']):
            login_user(_user)
            return {'message': f'User {_user.username} logged in.'}, 200
        else:
            return {'message': 'Check your username and password.'}, 400
    else:
        return login_validator.errors, 400


# route to register new users.
@app.route('/register', methods=['POST'])
def register():
    req_data = request.get_json()
    # Use login validator here as well, it is the same.
    if login_validator.validate(req_data):
        if User.query.filter_by(username=req_data['username']).first():
            return {'username': 'This username already exists'}, 400
        else:
            newUser = User(
                # Generate a random pass hash.
                username=req_data['username'],
                password=Bcrypt().generate_password_hash(req_data['password']).decode('utf-8'))

            db.session.add(newUser)
            db.session.commit()
            return {'message': f'User {newUser.username} created successfully'}, 200
    else:
        return login_validator.errors, 400


# Keep the session alive for 10 minutes
@app.before_request
def before_request():
    app.permanent_session_lifetime = datetime.timedelta(minutes=10)
