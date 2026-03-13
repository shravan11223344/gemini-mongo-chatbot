from pymongo import MongoClient
from config.settings import Settings

settings = Settings()

_client =MongoClient(settings.MONGO_DB_URI, tz_aware=True)
_db = _client[settings.MONGO_DB_NAME]

def get_collection(collection_name):
    return _db[collection_name]