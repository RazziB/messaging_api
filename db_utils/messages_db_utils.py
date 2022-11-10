from typing import List

from flask_login import current_user

from api_objects.message import Message
from db_utils.db_general_utils import get_collection
from general_utils.mongo_general_utils import remove_mongo_id


class MessagesDBUtils:
    TABLE_NAME = 'messages'
    MAX_FIND_AMOUNT = 30
    MIN_FIND_AMOUNT = 5

    def __init__(self):
        self.db = get_collection(self.TABLE_NAME)

    def insert_message(self, message: Message):
        self.db.insert_one(document=message.convert_to_dict())

    def get_messages_sent_to_user(self, user_id: str, amount, skip: int = 0,
                                  only_read_messages: bool = False) -> List[Message]:
        amount = int(amount)
        if amount <= self.MIN_FIND_AMOUNT:
            amount = self.MIN_FIND_AMOUNT
        if amount >= self.MAX_FIND_AMOUNT:
            amount = self.MAX_FIND_AMOUNT
        filter = {'receiver_id': user_id}
        if only_read_messages:
            filter.update({'is_read': True})
        results = list(self.db.find(filter=filter, limit=amount,
                                    sort={'date_sent': 1}, skip=skip))
        return [Message.from_dict(message_dict) for message_dict in results]

    def get_chats(self, base_user_id: str, contacts_ids: list, limit: int):
        facet_aggregations = {}
        for user_id in set(contacts_ids):
            facet_aggregations[user_id] = [
                {'$sort': {'date_sent': -1}},
                {'$match': {'$or':
                    [
                        {'$and': [{'receiver_id': base_user_id}, {'sender_id': user_id}]},
                        {'$and': [{'receiver_id': user_id}, {'sender_id': base_user_id}]}
                    ]}
                },
                {'$limit': limit},
                {'$project': {'_id': 0}}
            ]
        results = self.db.aggregate(pipeline=[{'$facet': facet_aggregations}])
        if results:
            return list(results)[0]

    def get_recent_chats(self, user_id):
        results = list(self.db.aggregate([
            {'$match': {'$or': [
                {'sender_id': user_id},
                {'receiver_id': user_id}
            ]}},

            {'$group': {'_id': {'$cond': [{'$eq': ['$receiver_id', user_id]}, '$sender_id', '$receiver_id']}}}

        ]
        ))
        friends_ids = [doc.get('_id') for doc in results]
        print(f'friends ids are : {friends_ids}')
        return friends_ids
