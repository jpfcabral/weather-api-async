from fastapi import FastAPI
from src.database import init_db, shutdown_db
from src.weather.routers import router as api_router
from src.config.settings import Settings

settings = Settings()

def create_web_app() -> FastAPI:
    ''' Create Web App '''
    application = FastAPI()
    application.include_router(api_router, prefix='/weather')
    return application

app = create_web_app()

@app.on_event('startup')
async def start():
    ''' All operations when web app startup '''
    init_db()

@app.on_event('shutdown')
async def disconnect():
    ''' All operations when web app shutdown '''
    shutdown_db()
