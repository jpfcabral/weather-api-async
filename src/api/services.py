import requests

from src.config import Settings

settings = Settings()


class APIServices:
    '''
    Encapsulates all API related business logic
    '''
    def __init__(self) -> None:
        pass

    async def collect_weather_data(self, city_id: str):
        ''' Create a task to request weather data '''
        response = requests.post(
            f'{settings.OPEN_WEATHER_HOST}/data/2.5/weather?' \
            f'id={city_id}&appid={settings.OPEN_WEATHER_API_KEY}',
            timeout=10
        )

        return response.json()
