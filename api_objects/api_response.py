from api_objects.api_errors import ApiErrors
from api_objects.frozen_object import FrozenObject


class ApiResponse(FrozenObject):
    def __init__(self, ok: bool = True, error: ApiErrors = None, description: str = None):
        self.ok: bool = ok
        self.error: ApiErrors = error
        self.description: str = description
