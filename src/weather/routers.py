from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from src.weather.services import WeatherServices

router = APIRouter()

@cbv(router)
class WeatherRouters:
    '''
    Encapsulates all API related routers

    Args:
        api_service (APIServices): Object to perform api services

    Attributes:
        api_service (APIServices): Internal object to perform api services
    '''
    def __init__(self) -> None:

        self.api_service = WeatherServices()

    @router.post('/')
    async def collect_weather_data(self, user_id: int):
        ''' This router runs a service to collect weather data '''
        return await self.api_service.collect_weather_data_and_save(user_id)

    @router.get('/')
    async def get_task_status(self, user_id: int):
        ''' Get status for a celery task '''
        return await self.api_service.get_task_status(user_id)
