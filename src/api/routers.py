from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from src.api.services import APIServices

router = APIRouter()

@cbv(router)
class APIRouters:
    '''
    Encapsulates all API related routers

    Args:
        api_service (APIServices): Object to perform api services

    Attributes:
        api_service (APIServices): Internal object to perform api services
    '''
    def __init__(
        self,
        api_service: APIServices = Depends(APIServices)
        ) -> None:

        self.api_service = api_service

    @router.post('/')
    async def collect_weather_data(self, user_id: int):
        ''' This router runs a service to collect weather data '''
        return await self.api_service.collect_weather_data(user_id)
