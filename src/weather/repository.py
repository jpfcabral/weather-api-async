from typing import Dict
from mongoengine.errors import NotUniqueError
from fastapi import HTTPException
from src.weather.models import Weather, WeatherData, WeatherDataModel, WeatherModel

class WeatherRepository:
    """
    Provide database abstraction operations to
    weather related data
    """

    def insert(self, data: WeatherModel) -> Dict:
        '''
        Used to insert weather data in database

        Args:
            data (WeatherModel): weather data to insert.
        Returns:
            Dict: inserted weather data
        '''
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
        '''
        Get a document from database by user_id field

        Args:
            user_id (int): User identifier.
        Returns:
            Dict: Related weather data
        '''
        try:
            weather = list(Weather.objects(user_id=user_id))[0]
            weather_dict = weather.to_mongo().to_dict()
            weather_dict['id'] = str(weather_dict['_id'])
            del weather_dict['_id']
        except:
            return None

        return weather_dict

    def insert_city_weather_data(self, user_id: int, weather_data: WeatherDataModel) -> None:
        '''
        Insert city weather data to a specific user id

        Args:
            user_id (int): User identifier.
            weather_data (WeatherDataModel): Related city weather data.
        Returns:
            Dict: Related weather data
        '''
        weather = Weather.objects(user_id=user_id).first()
        weather.weather_data.append(WeatherData(**weather_data.dict()))
        weather.save()

    def update_task_id(self, user_id: int, task_id: str) -> Dict:
        '''
        Update task id field for a specific user id

        Args:
            user_id (int): User identifier.
            task_id (str): Task identidier.
        Returns:
            Dict: Related weather data
        '''
        Weather.objects(user_id=user_id).update_one(set__task_id=task_id)
        return self.read_by_user_id(user_id)
