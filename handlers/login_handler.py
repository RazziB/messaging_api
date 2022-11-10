from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user

from api_objects.api_errors import ApiErrors
from api_objects.api_exceptions import ApiException
from api_objects.api_response import ApiResponse
from api_objects.user import User
from db_utils.sid_db_utils import SIDDBUtils
from db_utils.users_db_utils import UsersDBUtils
from messaging_api import login_manager
from validators import user_validators
from validators.user_validators import UserValidator


class LoginHandler:
    db_utils = UsersDBUtils()

    def __init__(self):
        self.user_validator = UserValidator()
        self.sid_db_utils = SIDDBUtils()

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return LoginHandler.db_utils.get_user_by_id(user_id=user_id)

    def login_user(self, login_data: dict) -> dict:
        print(f"received data: {login_data}")
        username = login_data.get(UserValidator.USERNAME_INPUT)
        password = login_data.get(UserValidator.PASSWORD_INPUT)

        user = self.db_utils.get_user_by_username(username=username)
        if user is None:
            raise ApiException(error=ApiErrors.BAD_LOGIN, description=f'Username: {username} or password: {password}'
                                                                      f' are wrong.')

        if self.__is_password_correct(user=user, password=password):
            results = login_user(user)
            return ApiResponse(description=f'User: {user.username} logged in successfully').convert_to_dict()
        else:
            raise ApiException(error=ApiErrors.BAD_LOGIN, description=f'Username: {username} or password: {password}'
                                                                      f' are wrong.')

    @staticmethod
    def __is_password_correct(user: User, password: str) -> bool:
        if Bcrypt().check_password_hash(pw_hash=user.encrypted_password, password=password):
            return True
        return False

    def save_new_user_sid(self, user_id: str, sid: str):
        self.sid_db_utils.insert_sid(user_id=user_id, sid=sid)
