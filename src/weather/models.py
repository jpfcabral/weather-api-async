from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import mongoengine as me


class WeatherData(me.EmbeddedDocument):
    city_id = me.IntField()
    temp = me.DecimalField()
    humidity = me.DecimalField()


class Weather(me.Document):
    ''' Weather database repository '''
    user_id = me.IntField(unique=True)
    request_datetime = me.DateField()
    task_id = me.StringField()
    weather_data = me.ListField()


class WeatherDataModel(BaseModel):
    ''' Weather Data View '''
    city_id: int
    temp: float
    humidity: int


class WeatherModel(BaseModel):
    ''' Weather Schema Model '''
    user_id: int
    request_datetime: datetime
    task_id: Optional[str]
    weather_data: Optional[WeatherDataModel]
