import datetime
import logging

from flask_cors import CORS
from flask import request, jsonify
from flask_login import current_user, login_required, logout_user
from flask_socketio import emit, disconnect

from api_objects.api_exceptions import ApiException
from api_objects.message import Message
from handlers.ApiHandler import ApiHandler
# from messaging_api.models import User, Message
from messaging_api import app, login_manager, socketio
from flask_bcrypt import Bcrypt

CORS(app)
api_handler = ApiHandler()

import functools


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped

@socketio.on_error_default
def handle_socket_exception(ex):
    app.logger.exception(msg="error occured")
    if isinstance(ex, ApiException):
        if ex.soc_listener:
            app.logger.info(msg="send emit ")
            emit(ex.soc_listener, ex.description)



@app.errorhandler(ApiException)
def handle_api_exception(ex: ApiException):
    print(f'api error: {str(ex)}')
    app.logger.exception(msg="error occured")
    app.logger.info(msg="Trying to ")
    if ex.soc_listener:
        app.logger.info(msg="send emit ")
        emit(ex.soc_listener, ex.description)
    return ex.convert_to_dict(), ex.status_code


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

#
# @app.errorhandler(Exception)
# def handle_general_exception(ex):
#     logging.exception(msg='General server error')
#     print(f'General server error: {str(ex)}')
#     return jsonify('General Server Error'), 500


# Route to write a message
@app.route('/message', methods=['POST'])
@login_required
def send_message():
    req_data = request.get_json()
    response = api_handler.messages_handler.send_message(message_data=req_data)
    return jsonify(response.convert_to_dict())


@app.route('/get_contacts_list', methods=['GET'])
@login_required
def get_contacts_list():
    response = api_handler.messages_handler.get_contact_list()
    print(f'contact list is : {response}')
    return jsonify(response)


@app.route('/get_chats', methods=['POST'])
@login_required
def get_chats():
    users_ids = request.json.get('users_ids')
    response = api_handler.messages_handler.get_chats_from_contacts(users_ids=users_ids)
    return jsonify(response)


# Route to get all messages that the current logged in user received / sent.
@app.route('/message/<int:page>')
@login_required
def get_messages(page):
    messages_batch: list = api_handler.messages_handler.get_user_messages_by_batches(page)
    return jsonify(messages_batch)


@app.route('/get_messages_from_list_of_users')
@login_required
def get_messages_from_contacts():
    list_of_users_ids = request.json.get('users_ids_list')
    api_handler.messages_handler.get_messages_from_contacts(list_of_users_ids)


# Route to get all unread messages the current user logged in has received.
# @app.route('/get_unread')
# def get_unread():
#     api_handler.messages_handler.get_unread_user_messages()
#     # if not current_user.is_authenticated:
#     #     return jsonify({'message': 'You need to be logged in for that.'}), 401
#     # else:
#     #     # get a list of all unread messages that the current user received.
#     #     unread = list(filter((lambda msg: msg.read is False), current_user.messages_received))
#     #     # turn each message to a dictionary.
#     #     unread = [Message.as_dict(msg) for msg in unread]
#     #     return jsonify(unread), 200


# Route to get the last unread message sent to the currently logged in user.
@app.route('/read_message')
def read_message():
    return_msg = None
    if not current_user.is_authenticated:
        return jsonify({'message': 'You need to be logged in for that.'}), 401
    else:
        # Get the last ( by id ) unread message the current user received. Sorry for the long line.
        msg = Message.query.filter_by(read=False, receiver=current_user.username).order_by(desc(Message.id)).first()
        if msg:
            return_msg = Message.as_dict(msg)
            msg.read = True
        db.session.commit()
        return jsonify(return_msg) or jsonify({'message': 'No unread messages.'}), 200


# Route to delete a message by id. This route does not make use of any request-body.
@app.route('/delete/<req_id>', methods=['DELETE'])
def delete_message(req_id):
    if not current_user.is_authenticated:
        return jsonify({'message': 'You need to be logged in for that.'}), 401
    msg = Message.query.filter_by(id=req_id).first()
    if msg and msg.sender_user_id == current_user.username:
        db.session.delete(msg)
        db.session.commit()
        return jsonify({'message': 'message was deleted.'}), 200
    elif msg:
        # Message sender is not current user.
        return jsonify({'message': 'You are not authorized.'}), 403
    else:
        return jsonify({'message': "Message does not exist."}), 400


@login_manager.unauthorized_handler
def handle_unauthorized():
    return "You need to be logged in to do that", 401


# Route to log in based on existing users currently in the database.
@app.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    response = api_handler.login_handler.login_user(login_data=req_data)
    print('login response: ', response)
    return jsonify(response)
    # # Form validated.
    # if login_validator.validate(req_data):
    #     # Get the user by username sent in the request-body
    #     _user = User.query.filter_by(username=req_data['username']).first()
    #     # User must exist in DB, and passwords must match.
    #     if _user and Bcrypt().check_password_hash(_user.password, req_data['password']):
    #         login_user(_user)
    #         return jsonify({'message': f'User {_user.username} logged in.'}), 200
    #     else:
    #         return jsonify({'message': 'Check your username and password.'}), 400
    # else:
    #     return jsonify(login_validator.errors), 400


# route to register new users.
@app.route('/register', methods=['POST'])
def register():
    req_data = request.get_json()
    response = api_handler.register_handler.register_new_user(user_data=req_data)
    return jsonify(response)


@app.route('/')
def home():
    return "<center><h1>It's alive</h1></center>"


# Keep the session alive for 10 minutes
@app.before_request
def before_request():
    app.permanent_session_lifetime = datetime.timedelta(minutes=300)


@app.route("/logout")
@login_required
def logout():
    if not current_user.is_authenticated:
        return jsonify({'message': 'You need to be logged in for that.'}), 401
    logout_user()
    return jsonify({'message': 'logged out'})


# SOCKET IO


@socketio.on('connect_chats')
@authenticated_only
def connect_chats():
    sid = request.sid
    user_id = current_user.get_id()
    api_handler.login_handler.save_new_user_sid(sid=sid, user_id=user_id)


@socketio.on('send_message')
@authenticated_only
def send_message(json):
    print('send message received json:', json)
    results, message = api_handler.messages_handler.send_message(message_data=json, by_username=json.get('by_username'))
    print('message is :', message)
    if results.ok:
        emit('ack_send', {'ok': True, 'message': message.jsonify(), 'user_id': message.receiver_id}, to=request.sid)
        receiver_id = api_handler.messages_handler.get_receiver_id_from_message(message=json)
        if receiver_id:
            receiver_sid = api_handler.sid_handler.get_user_sid_from_user_id(user_id=receiver_id)
            if receiver_sid:
                emit('receive_message', {'user_id': current_user.get_id(), 'message': message.jsonify()}, to=receiver_sid)


@app.route('/get_my_id', methods=['GET'])
@login_required
def get_my_id():
    return jsonify({'my_id': current_user.get_id()})
