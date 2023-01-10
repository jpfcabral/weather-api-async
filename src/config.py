from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    '''
    Store environment variables
    '''
    API_VERSION: str = '0.0.1-alpha'
