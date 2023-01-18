from typing import Optional

from api_objects.profile_picture import ProfilePicture
from db_utils.db_general_utils import get_collection
import os

class PhotosDBUtils:
    PHOTOS_FOLDER = os.environ.get('PHOTOS_FOLDER')
    PROFILE_PICTURE_FOLDER_NAME = os.environ.get('PROFILE_PICTURE_FOLDER_NAME')
    PROFILE_PICTURE_TABLE_NAME = os.environ.get('PROFILE_PICTURE_TABLE_NAME', default='profile_pictures')

    def __init__(self):
        self.db = get_collection(collection_name=self.PROFILE_PICTURE_FOLDER_NAME)

    def get_profile_picture(self, user_id) -> Optional[ProfilePicture]:
        db_results = self.db.find_one(filter={'user_id': user_id})
        if db_results:
            return ProfilePicture.from_dict(data=db_results)

    def save_profile_picture(self, pic: ProfilePicture) -> None:
        self.db.delete_many(filter={'user_id': pic.user_id})
        db_results = self.db.insert_one(pic.convert_to_dict())
        # todo: check how to wrap db_results and return custom wrapper