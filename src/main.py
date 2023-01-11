from fastapi import FastAPI
from src.weather.routers import router as api_router
from src.config.settings import Settings

settings = Settings()

def create_web_app() -> FastAPI:
    ''' Create Web App '''
    application = FastAPI()
    application.include_router(api_router, prefix='/weather')
    return application

app = create_web_app()
