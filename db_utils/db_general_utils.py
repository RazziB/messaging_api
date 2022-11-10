import os
from flask_mongoengine import MongoEngine
from pymongo import MongoClient

from messaging_api import app, MONGO_IP, MONGO_PORT, DB_NAME

mongo_engine_db = MongoEngine(app)


def get_collection(collection_name: str):
    client = MongoClient(MONGO_IP, MONGO_PORT)
    return client[DB_NAME][collection_name]
