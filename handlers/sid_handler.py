from db_utils.sid_db_utils import SIDDBUtils


class SIDHandler:

    db_utils = SIDDBUtils()

    def get_user_sid_from_user_id(self, user_id: str):
        sid = self.db_utils.get_user_sid(user_id=user_id)
        if sid:
            return sid.sid
