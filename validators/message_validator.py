import re
from enum import Enum

from flask_login import current_user

from api_objects.api_errors import ApiErrors
from api_objects.api_exceptions import ApiException
from api_objects.user import User
from db_utils.users_db_utils import UsersDBUtils


class MessageValidator:
    MIN_MESSAGE_LENGTH = 1
    MAX_MESSAGE_LENGTH = 400
    MAX_SUBJECT_LENGTH = 20

    SENDER_ID = 'sender_id'
    RECEIVER_ID = 'receiver_id'
    CONTENT = 'content'
    USERNAME = 'username'

    def __init__(self):
        self.user_db_utils = UsersDBUtils()

    def validate_message_form(self, message_data: dict):
        if type(message_data) is not dict:
            raise ApiException(error=ApiErrors.BAD_REQUEST, description="Server Could not understand request")
        self.validate_user_exists_by_id(user_id=message_data.get(self.RECEIVER_ID))
        self.validate_content(content=message_data.get(self.CONTENT))
        return True

    def validate_message_form_by_username(self, message_data):
        if type(message_data) is not dict:
            raise ApiException(error=ApiErrors.BAD_REQUEST, description="Server Could not understand request")
        user = self.validate_user_exists_by_username(username=message_data.get(self.USERNAME))
        if user.user_id == current_user.get_id():
            raise ApiException(error=ApiErrors.SAME_USER, description="cannot send message to yourself.",
                               soc_listener='err_msg')
        message_data[self.RECEIVER_ID] = user.user_id
        self.validate_content(content=message_data.get(self.CONTENT))
        return True

    def validate_user_exists_by_id(self, user_id: str) -> User:
        user = self.user_db_utils.get_user_by_id(user_id=user_id)
        if user:
            if user.user_id == current_user.get_id():
                raise ApiException(error=ApiErrors.SAME_USER, description="cannot send message to yourself.",
                                   soc_listener='err_msg')
            return user
        raise ApiException(error=ApiErrors.BAD_USER_ID, description='Could not find user wanted.')

    def validate_content(self, content: str):
        if len(re.sub(r'[\n\t\s]', '', content)) < self.MIN_MESSAGE_LENGTH:
            raise ApiException(error=ApiErrors.CONTENT_TOO_SHORT,
                               description=f'Content of message is too short, minimum of {self.MIN_MESSAGE_LENGTH}'
                                           f' characters')
        if len(content) < self.MIN_MESSAGE_LENGTH:
            raise ApiException(error=ApiErrors.CONTENT_TOO_SHORT,
                               description=f'Content of message is too short, minimum of {self.MIN_MESSAGE_LENGTH}'
                                           f' characters')

        if len(content) > self.MAX_MESSAGE_LENGTH:
            raise ApiException(error=ApiErrors.CONTENT_TOO_LONG,
                               description=f'Content of message is too long, maximum of {self.MAX_MESSAGE_LENGTH}'
                                           f' characters')

    def validate_subject(self, subject: str):
        if len(subject) > self.MAX_SUBJECT_LENGTH:
            raise ApiException(error=ApiErrors.CONTENT_TOO_LONG,
                               description=f'Content of subject is too long, maximum of {self.MAX_SUBJECT_LENGTH}')

    def validate_user_exists_by_username(self, username) -> User:
        user = self.user_db_utils.get_user_by_username(username=username)
        if user:
            return user
        raise ApiException(error=ApiErrors.NO_USERNAME, description="Username does not exist", soc_listener='err_msg')
