import datetime
import os
from builtins import object
from typing import List
from uuid import uuid4

from flask_login import current_user

from api_objects.api_errors import ApiErrors
from api_objects.api_exceptions import ApiException
from api_objects.api_response import ApiResponse
from api_objects.message import Message
from db_utils.messages_db_utils import MessagesDBUtils
from db_utils.users_db_utils import UsersDBUtils
from handlers.base_handler import BaseApiHandler
from validators.message_validator import MessageValidator


class MessagesHandler(BaseApiHandler):
    GET_MESSAGES_AMOUNT_PER_BATCH = os.environ.get('GET_MESSAGES_AMOUNT_PER_BATCH', default=15)
    NUM_OF_MESSAGES_PER_CHAT_AT_STARTUP = os.environ.get('NUM_OF_MESSAGES_PER_CHAT_AT_STARTUP', default=30)

    def __init__(self):
        self.user_db_utils = UsersDBUtils()
        self.db_utils = MessagesDBUtils()
        self.validator = MessageValidator()

    def get_contact_list(self):
        users_ids = self.db_utils.get_recent_chats(user_id=current_user.get_id())
        users = self.user_db_utils.get_users_by_ids(user_ids=users_ids)
        return [user.convert_to_dict() for user in users]

    def get_chats_from_contacts(self, users_ids: list):
        current_user_id = current_user.get_id()
        chats: List[dict] = self.db_utils.get_chats(base_user_id=current_user_id,
                                                    contacts_ids=users_ids,
                                                    limit=self.NUM_OF_MESSAGES_PER_CHAT_AT_STARTUP)
        return chats

    def get_messages_sent_to_user_by_page(self, user_id: str,
                                          page: int, only_read_messages: bool = False) -> list[Message]:
        messages_list = self.db_utils.get_messages_sent_to_user(user_id=user_id, amount=self.MESSAGES_PER_PAGE,
                                                                skip=page * self.MESSAGES_PER_PAGE,
                                                                only_read_messages=only_read_messages)
        return messages_list

    def send_message(self, message_data: dict, by_username: bool):
        if by_username:
            return self._send_message_by_username(message_data)
        else:
            return self._send_message_by_id(message_data)

    def _send_message_by_id(self, message_data):
        if self.validator.validate_message_form(message_data=message_data):
            new_message = self.prepare_new_message(data=message_data)
            self.db_utils.insert_message(message=new_message)
            return ApiResponse(), new_message
        return ApiResponse(ok=False, error=ApiErrors.UNKNOWN_ERROR, description='Unknown error validating message form')

    def _send_message_by_username(self, message_data):
        if self.validator.validate_message_form_by_username(message_data=message_data):
            new_message = self.prepare_new_message(data=message_data)
            self.db_utils.insert_message(message=new_message)
            return ApiResponse(), new_message
        return ApiResponse(ok=False, error=ApiErrors.UNKNOWN_ERROR, description='Unknown error validating message form')

    def get_user_messages_by_batches(self, page):
        messages_batch = self.db_utils.get_messages_sent_to_user(user_id=current_user.get_id(),
                                                                 amount=self.GET_MESSAGES_AMOUNT_PER_BATCH,
                                                                 skip=page * self.GET_MESSAGES_AMOUNT_PER_BATCH)
        return messages_batch

    def prepare_new_message(self, data) -> Message:
        return Message(message_id=str(uuid4()),
                       content=data.get(self.validator.CONTENT),
                       sender_id=current_user.get_id(),
                       receiver_id=data.get(self.validator.RECEIVER_ID),
                       send_date=datetime.datetime.now(),
                       is_read=False)

    def get_receiver_id_from_message(self, message):
        if type(message) is dict:
            return message.get(self.validator.RECEIVER_ID)
        elif isinstance(message, Message):
            return message.receiver_id

    # def get_unread_user_messages(self):
