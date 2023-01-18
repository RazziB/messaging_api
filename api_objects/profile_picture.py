from api_objects.frozen_object import FrozenObject


class ProfilePicture(FrozenObject):

    def __init__(self,
                 user_id,
                 path):
        self.user_id = user_id
        self.path = path
