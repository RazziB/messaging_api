from api_objects.api_errors import ApiErrors
from api_objects.api_exceptions import ApiException
from db_utils.users_db_utils import UsersDBUtils


class UserValidator:
    USERNAME_INPUT = 'username'
    PASSWORD_INPUT = 'password'

    MIN_PASSWORD_LENGTH = 5
    MAX_PASSWORD_LENGTH = 15
    MAX_USERNAME_LENGTH = 12
    ALLOWED_USERNAME_CHARACTERS = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    MIN_USERNAME_LENGTH = 4

    def __init__(self):
        self.db_utils = UsersDBUtils()

    def validate_username(self, username):

        if len(username) < self.MIN_USERNAME_LENGTH:
            raise ApiException(error=ApiErrors.USERNAME_TOO_SHORT,
                               description=f'Username length must be between '
                                           f'{self.MIN_USERNAME_LENGTH} and {self.MAX_USERNAME_LENGTH}')

        if len(username) > self.MAX_USERNAME_LENGTH:
            raise ApiException(error=ApiErrors.USERNAME_TOO_LONG,
                               description=f'Username length must be between '
                                           f'{self.MIN_USERNAME_LENGTH} and {self.MAX_USERNAME_LENGTH}')

        bad_chars = [letter for letter in username if letter not in self.ALLOWED_USERNAME_CHARACTERS]
        if bad_chars:
            raise ApiException(error=ApiErrors.BAD_USERNAME_CHARACTERS,
                               description=f'Bad characters in username: {bad_chars}. Only letters and numbers allowed')

    def validate_password(self, password):
        if len(password) < self.MIN_USERNAME_LENGTH:
            raise ApiException(error=ApiErrors.PASSWORD_TOO_SHORT,
                               description=f'Password length must be between '
                                           f'{self.MIN_PASSWORD_LENGTH} and {self.MAX_PASSWORD_LENGTH}')

        if len(password) > self.MAX_PASSWORD_LENGTH:
            raise ApiException(error=ApiErrors.PASSWORD_TOO_LONG,
                               description=f'Password length must be between '
                                           f'{self.MIN_PASSWORD_LENGTH} and {self.MAX_PASSWORD_LENGTH}')

    def validate_new_username(self, username):
        self.validate_username(username=username)
        if self.db_utils.is_username_already_exists(username=username) is True:
            raise ApiException(error=ApiErrors.USERNAME_ALREADY_EXISTS,
                               description=f'Username: {username} is taken.')
