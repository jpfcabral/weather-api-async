from datetime import datetime
from typing import Dict

from fastapi import HTTPException
from celery.result import AsyncResult, GroupResult
from celery import group

from src.config.city_ids import CITY_IDS
from src.config.settings import Settings
from src.weather.models import WeatherModel
from src.weather.repository import WeatherRepository
from src.weather.tasks import request_weather_data

settings = Settings()


class WeatherServices:
    """
    Provide all logic operations from weather related data

    Attributes:
    repository (WeatherRepository): dependencie to perform database operations
    """
    def __init__(self, repository: WeatherRepository = WeatherRepository()) -> None:
        self.repository = repository

    async def collect_weather_data_and_save(self, user_id: int) -> Dict:
        """
        Get user id and perform the business rules to celery
        task creation and data storage in database

        Args:
            user_id (int): User identifier.
        Returns:
            Dict: User and task state from database
        """
        tasks = []

        for city_id in CITY_IDS:
            tasks.append(
                request_weather_data.si(
                    user_id=user_id,
                    city_id=city_id,
                )
            )

        task_group = group(tasks)
        task_group_result: AsyncResult = task_group.apply_async()
        task_id = task_group_result.id

        weather = WeatherModel(
            user_id=user_id,
            request_datetime=datetime.now(),
            task_id=task_id
            )

        if self.repository.read_by_user_id(user_id):
            return self.repository.update_task_id(user_id, task_id)

        weather_db = self.repository.insert(weather)
        return weather_db

    async def get_task_status(self, user_id: int) -> Dict:
        """
        Get user id and perform all business rules about
        a user task state

        Args:
            user_id (int): User identifier.
        Returns:
            Dict: User and task state from database
        """
        response = {}
        weather_doc = self.repository.read_by_user_id(user_id)

        if not weather_doc:
            raise HTTPException(status_code=404, detail='User not found')

        result = AsyncResult(weather_doc['task_id'])
        response['status'] = result.state

        if response['status'] == 'PROGRESS':
            response = response | result.info

        return response | weather_doc
