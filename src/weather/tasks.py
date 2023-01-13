from time import sleep
from typing import List

import requests
from celery import Celery
from celery.utils.log import get_logger
from celery import Task
from fastapi import HTTPException

from src.config.settings import Settings
from src.config.city_ids import CITY_IDS
from src.weather.repository import WeatherRepository
from src.weather.models import WeatherDataModel
from src.database import init_db

logger = get_logger(__name__)
settings = Settings()

app = Celery(
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BACKEND_URL
    )


class WeatherRequestTask(Task):
    """
    Implement and configure all operations for weather request.

    Attributes:
    weather_repository (WeatherRepository): dependencie to perform database operations
    autoretry_for (tuple): List for all exceptions accepted to retry for
    max_retries (int): Max retries when task failed
    retry_backoff (bool): Use exponencial backoff to retry task
    retry_backoff_max (int): Max time to wait to retry
    """

    def __init__(
        self,
        weather_repository: WeatherRepository = WeatherRepository()
        ) -> None:

        # Task configuration
        self.autoretry_for = (Exception,)
        self.max_retries = 5
        self.retry_backoff = True
        self.retry_backoff_max = 700

        # Init dependencies
        init_db()
        self.weather_repository = weather_repository

    def store_weather_data_list(self, user_id: int, data_list: List):
        """
        Store Weather data from Open Weather to a weather document

        Args:
            user_id (int): User identifier.
            data_list (List): Contains the request responses from OpenWeather
        """
        for data in data_list:
            city_id = data['id']
            weather_data = data['main'] | {'city_id': city_id}
            self.weather_repository.insert_weather_data(user_id, WeatherDataModel(**weather_data))


    def request_open_weather_api(self, city_id: int):
        """
        This task perform request to Open Weather

        Args:
            city_id (int): City identifier.
        """
        response = requests.post(
            f'{settings.OPEN_WEATHER_HOST}/data/2.5/weather?' \
            f'id={city_id}&appid={settings.OPEN_WEATHER_API_KEY}' \
            f'&units=metric',
            timeout=10
        )

        # Check response status
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail='Error request weather data'
                )

        logger.info(
            'Request City Weather | City ID : {0} | Response status: {1}'.format(city_id, response.status_code)
            )
        return response

@app.task(bind=True, base=WeatherRequestTask)
def request_weather_data(self, user_id: int, req_delay: float = 1.0):
    """
    This task perform requests to Open Weather API
    and store the response into mongodb by user_id

    Args:
        user_id (int): User identifier.
        req_delay (float): Delay for each request to open weather.
    """
    count = 0
    weather_data_list = []

    for city_id in CITY_IDS:

        response = self.request_open_weather_api(city_id)
        weather_data_list.append(response.json())

        # Update task state
        percentage = round(count / len(CITY_IDS), 3)
        self.update_state(state='PROGRESS', meta={'progress': percentage})
        count += 1
        sleep(req_delay)

    self.store_weather_data_list(user_id, weather_data_list)
    self.update_state(state='COMPLETED', meta={'progress': percentage})
