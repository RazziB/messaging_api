from datetime import datetime, timedelta

from flask_login import UserMixin

from api_objects.frozen_object import FrozenObject


class User(UserMixin, FrozenObject):
    MIN_DAYS_ACTIVE = 365

    def __init__(self,
                 user_id: str,
                 username: str,
                 encrypted_password: str,
                 last_active: datetime
                 ):
        self.user_id = user_id
        self.username = username
        self.encrypted_password = encrypted_password

    def get_id(self):
        return self.user_id

    def convert_to_dict(self):
        user_dict = super().convert_to_dict()
        user_dict['encrypted_password'] = str(user_dict.get('encrypted_password'))
        user_dict['key'] = user_dict.get('user_id')

        return user_dict