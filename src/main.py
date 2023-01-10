from fastapi import FastAPI
from src.api.routers import router as api_router
from src.config import Settings

settings = Settings()

def create_web_app() -> FastAPI:
    ''' Create Web App '''
    application = FastAPI()
    application.include_router(api_router, prefix='/api')
    return application

app = create_web_app()
