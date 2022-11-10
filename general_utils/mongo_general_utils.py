def remove_mongo_id(data: dict):
    data.pop('_id')
