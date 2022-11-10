from flask_login import user_loaded_from_request

from api_objects.api_errors import ApiErrors
from api_objects.api_exceptions import ApiException
from api_objects.user import User
from db_utils.db_general_utils import get_collection
from messaging_api import login_manager


class UsersDBUtils:
    TABLE_NAME = 'users'
    db = get_collection(collection_name=TABLE_NAME)

    def __init__(self):
        pass

    def insert_user(self, user: User):
        self.db.insert_one(user.convert_to_dict())

    def is_username_already_exists(self, username: str) -> bool:
        if self.db.find_one(filter={'username': username}) is None:
            return False
        return True

    def get_user_by_username(self, username: str):
        user_data = self.db.find_one(filter={'username': username})
        if user_data:
            return User.from_dict(user_data)

    def get_user_by_id(self, user_id: str):
        user_data = self.db.find_one(filter={'user_id': user_id})
        if user_data:
            return User.from_dict(user_data)
        else:
            raise ApiException(error=ApiErrors.BAD_USER_ID, description='User ID was not found.')

    def get_users_by_ids(self, user_ids):
        users_dicts = self.db.find(filter={'user_id': {'$in': user_ids}})
        users = [User.from_dict(user_dict) for user_dict in users_dicts]
        return users