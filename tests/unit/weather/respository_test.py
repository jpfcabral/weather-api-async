from datetime import datetime
import pytest
from fastapi import HTTPException
from src.weather.repository import WeatherRepository
from src.weather.models import Weather, WeatherDataModel, WeatherModel

@pytest.fixture
def weather_repository():
    return WeatherRepository()

def test_insert(weather_repository: WeatherRepository):
    weather = WeatherModel(
        user_id=123,
        request_datetime=datetime.now(),
        task_id='task-id'
    )

    weather_repository.insert(weather)

    weather_db = Weather.objects(user_id=123)

    assert len(list(weather_db)) == 1

def test_insert_duplicated_user_id(weather_repository: WeatherRepository):
    data = WeatherModel(
        user_id=123,
        request_datetime=datetime.now(),
        task_id='task-id'
    )
    Weather(**data.dict()).save()

    with pytest.raises(HTTPException):
        another_weather = WeatherModel(
            user_id=123,
            request_datetime=datetime.now(),
            task_id='task-id'
        )

        weather_repository.insert(another_weather)

def test_read_by_user_id(weather_repository: WeatherRepository):
    data = WeatherModel(
        user_id=123,
        request_datetime=datetime.now(),
        task_id='task-id'
    )
    Weather(**data.dict()).save()
    weather = weather_repository.read_by_user_id(123)

    assert weather['id'] is not None
    assert weather['user_id'] == 123
    assert isinstance(weather['request_datetime'], datetime)
    assert weather['task_id'] == 'task-id'

def test_read_by_user_id_error(weather_repository: WeatherRepository):

    weather = weather_repository.read_by_user_id(123)

    assert weather is None

def test_insert_weather_data(weather_repository: WeatherRepository):
    data = WeatherModel(
        user_id=123,
        request_datetime=datetime.now(),
        task_id='task-id'
    )
    Weather(**data.dict()).save()

    weather_data = WeatherDataModel(
        city_id=456,
        temp=33.6,
        humidity=24
    )

    weather_repository.insert_city_weather_data(123, weather_data)

def test_update_task_id(weather_repository: WeatherRepository):
    data = WeatherModel(
        user_id=123,
        request_datetime=datetime.now(),
        task_id='task-id'
    )
    Weather(**data.dict()).save()

    weather = weather_repository.update_task_id(123, 'new-task-id')

    assert weather['task_id'] == 'new-task-id'
