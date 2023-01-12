from mongoengine import connect, disconnect
from src.config.settings import Settings

settings = Settings()

def init_db():
    ''' Generate Mongo db connection  '''
    connect(
        host=settings.DB_HOST,
        db=settings.DB_NAME
    )

def shutdown_db():
    ''' Close Mongo db connection  '''
    disconnect()
