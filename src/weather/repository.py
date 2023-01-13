from typing import Dict
from mongoengine.errors import NotUniqueError
from fastapi import HTTPException
from src.weather.models import Weather, WeatherData, WeatherDataModel, WeatherModel

class WeatherRepository:
    ''' Weather database repository '''

    def insert(self, data: WeatherModel) -> Dict:
        ''' Used to insert data in database '''
        try:
            weather_db = Weather(**data.dict())
            weather_db.save().to_mongo()
            weather_dict = weather_db.to_mongo().to_dict()

            weather_dict['id'] = str(weather_dict['_id'])
            del weather_dict['_id']

            return weather_dict
        except NotUniqueError:
            raise HTTPException(status_code=422, detail='User already exists')

    def read_by_user_id(self, user_id: int) -> Dict:
        ''' Get a document from database by user_id field'''
        try:
            weather = list(Weather.objects(user_id=user_id))[0]
            weather_dict = weather.to_mongo().to_dict()
            weather_dict['id'] = str(weather_dict['_id'])
            del weather_dict['_id']
        except:
            return None

        return weather_dict

    def insert_weather_data(self, user_id: int, weather_data: WeatherDataModel):
        weather = Weather.objects(user_id=user_id).first()
        weather.weather_data.append(WeatherData(**weather_data.dict()))
        weather.save()
