from api_objects.frozen_object import FrozenObject


class SID(FrozenObject):
    def __init__(self, user_id: str, sid):

        self.user_id = user_id
        self.sid = sid