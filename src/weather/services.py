from datetime import datetime
from fastapi import HTTPException
from celery.result import AsyncResult
from src.config.settings import Settings
from src.weather.models import WeatherModel
from src.weather.repository import WeatherRepository
from src.weather.tasks import request_weather_data

settings = Settings()


class WeatherServices:
    '''
    Encapsulates all API related business logic
    '''
    def __init__(self, repository: WeatherRepository = WeatherRepository()) -> None:
        self.repository = repository

    async def collect_weather_data_and_save(self, user_id: int):
        ''' Create a task to request weather data '''
        task_id = request_weather_data.delay(user_id).id

        weather = WeatherModel(
            user_id=user_id,
            request_datetime=datetime.now(),
            task_id=task_id
            )

        weather_db = self.repository.insert(weather)

        return weather_db

    async def get_task_status(self, user_id: int):
        ''' Get status from a task created '''
        response = {}
        weather_doc = self.repository.read_by_user_id(user_id)

        if not weather_doc:
            raise HTTPException(status_code=404, detail='User not found')

        result = AsyncResult(weather_doc['task_id'])
        response['status'] = result.state

        if response['status'] == 'PROGRESS':
            response = response | result.info

        return response | weather_doc
