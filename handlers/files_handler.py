import io
import logging
import os
import imghdr
from typing import Tuple
from uuid import uuid4

import PIL.Image
from flask_login import current_user
from werkzeug.datastructures import FileStorage

from api_objects.api_errors import ApiErrors
from api_objects.api_exceptions import ApiException
from api_objects.profile_picture import ProfilePicture
from db_utils.photos_db_utils import PhotosDBUtils


class FilesHandler:
    PHOTOS_FOLDER = os.environ.get('PHOTOS_FOLDER')
    PROFILE_PICTURE_FOLDER_NAME = os.environ.get('PROFILE_PICTURE_FOLDER_NAME')

    def __init__(self):
        self.photos_db = PhotosDBUtils()

    def upload_profile_picture(self, photo_obj: FileStorage):
        io_file, ext = self._validate_photo(photo_obj)
        user_folder, full_file_path = self._get_profile_photos_path(extension=ext)
        self.save_file(user_folder=user_folder, full_file_path=full_file_path, file=io_file)
        pic = ProfilePicture(user_id=current_user.user_id, path=full_file_path)
        self.photos_db.save_profile_picture(pic=pic)

    def _get_profile_photos_path(self, extension: str) -> Tuple[str, str]:
        user_id = current_user.get_id()
        return os.path.join(self.PHOTOS_FOLDER,
                            self.PROFILE_PICTURE_FOLDER_NAME,
                            user_id), os.path.join(self.PHOTOS_FOLDER,
                                                   self.PROFILE_PICTURE_FOLDER_NAME,
                                                   user_id,
                                                   f"{str(uuid4())}.{extension}")

    def save_file(self, user_folder, full_file_path, file: io.BytesIO):
        if not os.path.isdir(user_folder):
            os.mkdir(user_folder)
        with open(full_file_path, 'wb') as f:
            f.write(file.read())

    def _validate_photo(self, photo_obj: FileStorage) -> (io.BytesIO, str):
        try:
            file = io.BytesIO(photo_obj.read())
            p_type = imghdr.what(file)
            # if p_type not in ['png', 'jpeg']:
            #     raise Exception(f"profile photo was of type {p_type}")
            photo_obj.seek(0)
            img = PIL.Image.open(file)
            img.verify()
            file.seek(0)
            return file, p_type
        except Exception as e:
            raise ApiException(error=ApiErrors.BAD_PROFILE_PHOTO,
                               description="Profile image must be of type 'png' or 'jpg'."
                               ) from e

    def send_profile_photo(self, user_id: str) -> str:
        pic: ProfilePicture = self.photos_db.get_profile_picture(user_id=user_id)
        return pic.path
