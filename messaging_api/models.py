from messaging_api import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask_login import login_user, current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    messages_sent = db.relationship('Message', backref='msg_sender', lazy=True, foreign_keys='[Message.sender]')
    messages_received = db.relationship('Message', backref='msg_receiver', lazy=True, foreign_keys='[Message.receiver]')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sender = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    receiver = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(20), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    read = db.Column(db.Boolean, nullable=False, default=False)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
