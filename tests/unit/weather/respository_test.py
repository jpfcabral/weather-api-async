from datetime import datetime
import pytest
from fastapi import HTTPException
from src.weather.repository import WeatherRepository
from src.weather.models import Weather, WeatherModel

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
