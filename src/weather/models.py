from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from mongoengine import Document, StringField, IntField, DateField, ListField


class Weather(Document):
    ''' Weather database repository '''
    user_id = IntField(unique=True)
    request_datetime = DateField()
    task_id = StringField()
    weather_data = ListField()


class WeatherData(BaseModel):
    ''' Weather Data View '''
    city_id: int
    temperature_celsius: float
    humidity: int


class WeatherModel(BaseModel):
    ''' Weather Schema Model '''
    user_id: int
    request_datetime: datetime
    task_id: str
    weather_data: Optional[WeatherData]
