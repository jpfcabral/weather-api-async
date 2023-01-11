from datetime import datetime
from typing import Dict
import requests
from fastapi import Depends, HTTPException
from src.config.settings import Settings
from src.weather.repository import WeatherRepository
from src.weather.models import WeatherData, Weather

settings = Settings()


class WeatherServices:
    '''
    Encapsulates all API related business logic
    '''
    def __init__(self, repository: WeatherRepository = Depends(WeatherRepository)) -> None:
        self.repository = repository

    async def collect_weather_data_and_save(self, user_id: int, city_id: int):
        ''' Create a task to request weather data '''
        response = requests.post(
            f'{settings.OPEN_WEATHER_HOST}/data/2.5/weather?' \
            f'id={city_id}&appid={settings.OPEN_WEATHER_API_KEY}' \
            f'&units=metric',
            timeout=10
        )

        if response.status_code != 200:
            raise HTTPException(status_code=503, detail='3rd party API not available')

        data = response.json()['main']
        await self.save_weather_data(user_id, city_id, data)

        return response.json()

    async def save_weather_data(self, user_id: int, city_id: int, data: Dict):
        ''' Save weather data info in database '''
        weather_data = WeatherData(
            city_id=city_id,
            temperature_celsius=data['temp'],
            humidity=data['humidity']
            )
        weather = Weather(
            user_id=user_id,
            request_datetime=datetime.now(),
            weather_data=weather_data
            ).dict()

        doc_id = await self.repository.insert(weather)

        return doc_id
