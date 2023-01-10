from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from src.api.services import APIServices

router = APIRouter()

@cbv(router)
class APIRouter:
    def __init__(
        self,
        api_service: APIServices = Depends(APIServices)
        ) -> None:

        self.api_service = api_service

    @router.post('/')
    async def collect_weather_data(self, user_id: int):
        return await self.api_service.send_task(user_id)
