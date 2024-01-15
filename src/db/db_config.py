from pymongo import MongoClient, ReadPreference
from src.config import settings


client = MongoClient(settings.mongodb_url, replicaSet=settings.rs_name, read_preference=ReadPreference.PRIMARY)
db = client[settings.db_name]

