from datetime import datetime
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
    weather_data: WeatherData
