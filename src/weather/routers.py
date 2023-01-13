from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from src.weather.services import WeatherServices

router = APIRouter()

@cbv(router)
class WeatherRouters:
    '''
    Encapsulates all API related routers

    Attributes:
        api_service (APIServices): Internal object to perform api services
    '''
    def __init__(self) -> None:

        self.api_service = WeatherServices()

    @router.post('/')
    async def collect_weather_data(self, user_id: int):
        """
        Router to perform weather data extraction

        Args:
            user_id (int): User identifier.
        Returns:
            Dict: User and task state from database
        """
        return await self.api_service.collect_weather_data_and_save(user_id)

    @router.get('/')
    async def get_task_status(self, user_id: int):
        """
        Provide user task status

        Args:
            user_id (int): User identifier.
        Returns:
            Dict: User and task state from database
        """
        return await self.api_service.get_task_status(user_id)
