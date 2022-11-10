from api_objects.sid_object import SID
from db_utils.db_general_utils import get_collection


class SIDDBUtils:
    COLLECTION_NAME = 'user_to_sid'
    db = get_collection(collection_name=COLLECTION_NAME)

    def __init__(self):
        pass

    def get_user_sid(self, user_id):
        results = self.db.find_one({'user_id': user_id})
        if results:
            return SID.from_dict(results)

    def insert_sid(self, user_id, sid):
        results = self.db.update_one(filter={'user_id': user_id},
                                     update={'$set': {'sid': sid}})
        if results.matched_count == 0:
            new_sid = SID(user_id=user_id, sid=sid)
            self.db.insert_one(document=new_sid.convert_to_dict())

    def delete_sid(self, user_id):
        results = self.db.delete_one(filter={'user_id': user_id})
        pass
