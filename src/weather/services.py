from datetime import datetime
from fastapi import Depends
from src.config.settings import Settings
from src.weather.models import Weather
from src.weather.repository import WeatherRepository
from src.weather.tasks import request_weather_data

settings = Settings()


class WeatherServices:
    '''
    Encapsulates all API related business logic
    '''
    def __init__(self, repository: WeatherRepository = Depends(WeatherRepository)) -> None:
        self.repository = repository

    async def collect_weather_data_and_save(self, user_id: int):
        ''' Create a task to request weather data '''
        task_id = request_weather_data.delay(user_id).id

        weather = Weather(
            user_id=user_id,
            request_datetime=datetime.now(),
            task_id=task_id
            )

        self.repository.insert(weather.dict())

        return weather

    async def get_task_status(self, user_id: int):
        ''' Get status from a task created '''
        weather_doc = self.repository.read_by_user_id(user_id)

        res = request_weather_data.AsyncResult(weather_doc['task_id']).state
        print(res)
        return weather_doc
