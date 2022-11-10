from api_objects.api_errors import ApiErrors
from api_objects.frozen_object import FrozenObject


class ApiException(Exception):
    def __init__(self, error: ApiErrors,
                 status_code: int = 400,
                 description: str = None,
                 soc_listener: str = None):
        super(Exception, self).__init__()
        self.error = error
        self.status_code = status_code
        self.description = description
        self.soc_listener = soc_listener

    def convert_to_dict(self):
        return vars(self)
