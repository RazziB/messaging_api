from enum import Enum


class ApiErrors(str, Enum):
    SAME_USER = 'SAME_USER'
    BAD_REQUEST = 'BAD_REQUEST'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
    CONTENT_TOO_SHORT = 'CONTENT_TOO_SHORT'
    CONTENT_TOO_LONG = 'CONTENT_TOO_LONG'
    BAD_USER_ID = 'BAD_USER_ID'
    BAD_LOGIN = 'BAD_USERNAME'
    PASSWORD_TOO_LONG = 'PASSWORD_TOO_LONG'
    USERNAME_ALREADY_EXISTS = 'USERNAME_ALREADY_EXISTS'
    USERNAME_TOO_LONG = 'USERNAME_TOO_LONG'
    BAD_USERNAME_CHARACTERS = 'BAD_USERNAME_CHARACTERS'
    PASSWORD_TOO_SHORT = 'PASSWORD_TOO_SHORT'
    NO_PASSWORD = 'NO_PASSWORD'
    USERNAME_TOO_SHORT = 'USERNAME_TOO_SHORT'
    NO_USERNAME = 'NO_USERNAME'

