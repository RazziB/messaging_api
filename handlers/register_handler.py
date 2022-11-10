from uuid import uuid4

from flask_bcrypt import Bcrypt

from api_objects.api_errors import ApiErrors
from api_objects.api_exceptions import ApiException
from api_objects.api_response import ApiResponse
from api_objects.user import User
from db_utils.users_db_utils import UsersDBUtils
from handlers.base_handler import BaseApiHandler
from validators.user_validators import UserValidator


class RegisterHandler(BaseApiHandler):

    def __init__(self):
        self.db_utils = UsersDBUtils()
        self.validator = UserValidator()

    def register_new_user(self, user_data: dict) -> dict:
        if self.validate_new_user_data(data=user_data) is True:
            created_user = self.create_and_insert_new_user(user_data=user_data)
            return ApiResponse(description=f'User: {created_user.username} was created successfully.').convert_to_dict()

    def validate_new_user_data(self, data: dict) -> bool:
        username = data.get('username')
        password = data.get('password')

        self.validator.validate_new_username(username)
        self.validator.validate_password(password)
        return True

    def create_and_insert_new_user(self, user_data) -> User:
        username = user_data.get('username')
        password = user_data.get('password')

        new_user = User(user_id=str(uuid4()),
                        username=username,
                        encrypted_password=Bcrypt().generate_password_hash(password=password))
        self.db_utils.insert_user(user=new_user)
        return new_user
