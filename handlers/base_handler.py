import os


class BaseApiHandler:
    MESSAGES_PER_PAGE = os.environ.get('MESSAGES_PER_PAGE')
