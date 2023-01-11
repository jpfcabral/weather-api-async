from pymongo import MongoClient
from src.config.settings import Settings

settings = Settings()


db = MongoClient(host=settings.DB_HOST)[settings.DB_NAME]
