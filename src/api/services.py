import requests

from src.config import Settings

settings = Settings()


class APIServices:
    def __init__(self) -> None:
        pass

    async def send_task(self, city_id: str):
        
        response = requests.post(
            f'{settings.OPEN_WEATHER_HOST}/data/2.5/weather?id={city_id}&appid={settings.OPEN_WEATHER_API_KEY}'
        )

        return response.json()
