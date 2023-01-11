from pymongo import MongoClient
from src.config import Settings

settings = Settings()


db = MongoClient(host=settings.DB_HOST)[settings.DB_NAME]
