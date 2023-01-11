from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class WeatherData(BaseModel):
    ''' Weather Data View '''
    city_id: int
    temperature_celsius: float
    humidity: int


class Weather(BaseModel):
    ''' Weather Schema Model '''
    user_id: int
    request_datetime: datetime
    task_id: str
    weather_data: Optional[WeatherData]
