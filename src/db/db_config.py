from pymongo import MongoClient
from src.config import settings


client = MongoClient(settings.mongodb_url)
db = client[settings.db_name]
