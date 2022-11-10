import datetime

from api_objects.frozen_object import FrozenObject


class Message(FrozenObject):
    def __init__(self,
                 message_id: str,
                 content: str,
                 sender_id: str,
                 receiver_id: str,
                 send_date: datetime.datetime,
                 is_read: bool):
        self.message_id = message_id
        self.content = content
        self.receiver_id = receiver_id
        self.sender_id = sender_id
        self.date_sent = send_date
        self.is_read = is_read

    def jsonify(self):
        return {
            'message_id': self.message_id,
            'content': self.content,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'send_date': str(self.date_sent),
            'is_read': self.is_read
        }