from typing import Dict

from src.weather.models import Weather, WeatherModel

class WeatherRepository:
    ''' Weather database repository '''

    def insert(self, data: WeatherModel) -> Dict:
        ''' Used to insert data in database '''
        weather_db = Weather(**data.dict())
        weather_db.save().to_mongo()
        weather_dict = weather_db.to_mongo().to_dict()

        weather_dict['id'] = str(weather_dict['_id'])
        del weather_dict['_id']

        return weather_dict

    def read_by_user_id(self, user_id: int) -> Dict:
        ''' Get a document from database by user_id field'''
        weather = list(Weather.objects(user_id=user_id))[0]
        weather_dict = weather.to_mongo().to_dict()
        weather_dict['id'] = str(weather_dict['_id'])
        del weather_dict['_id']

        return weather_dict
