from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    '''
    Store environment variables
    '''
    API_VERSION: str = '0.0.1-alpha'
    OPEN_WEATHER_HOST: str = 'https://api.openweathermap.org'
    OPEN_WEATHER_API_KEY: str

    DB_HOST: str = 'mongodb://localhost:27017/'
    DB_NAME: str = 'test-db'

    CELERY_BROKER_URL: str = 'pyamqp://guest@localhost//'
    CELERY_BACKEND_URL: str = 'redis://localhost:6379/0'
