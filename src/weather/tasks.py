import requests
from celery import Celery
from celery.utils.log import get_logger
from src.config.settings import Settings
from src.config.city_ids import CITY_IDS
from src.weather.repository import WeatherRepository


weather_repository = WeatherRepository()
logger = get_logger(__name__)
settings = Settings()

app = Celery(
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BACKEND_URL
    )

@app.task(bind=True)
def request_weather_data(self, user_id: int):
    ''' Request all weather data async '''
    count = 0
    for city_id in CITY_IDS:
        response = requests.post(
            f'{settings.OPEN_WEATHER_HOST}/data/2.5/weather?' \
            f'id={city_id}&appid={settings.OPEN_WEATHER_API_KEY}' \
            f'&units=metric',
            timeout=10
        )
        count += 1
        percentage = round(count / len(CITY_IDS), 3)
        self.update_state(state='PROGRESS', meta={'progress': percentage})

        logger.info(response.status_code)

    self.update_state(state='COMPLETED', meta={'progress': percentage})
