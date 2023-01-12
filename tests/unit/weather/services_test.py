from datetime import datetime
from typing import Dict, Optional
import pytest
from pydantic import BaseModel
from src.weather.models import Weather, WeatherModel
from src.weather.services import WeatherServices

@pytest.fixture
def weather_services():
    return WeatherServices()

class TaskResult(BaseModel):
    id: str
    state: Optional[str]
    info: Optional[Dict]

@pytest.mark.asyncio
async def test_collect_weather_data_and_save(mocker, weather_services: WeatherServices):
    mocker.patch(
        'src.weather.tasks.request_weather_data.delay',
        return_value=TaskResult(id='456-456')
    )

    task = await weather_services.collect_weather_data_and_save(123)

    assert task['user_id'] == 123
    assert task['task_id'] == '456-456'

@pytest.mark.asyncio
async def test_get_task_status_progress(mocker, weather_services: WeatherServices):
    mocker.patch(
        'src.weather.services.AsyncResult',
        return_value=TaskResult(
            id='456-456',
            state='PROGRESS',
            info={'progress': 0.161}
        )
    )

    Weather(
        user_id=123,
        request_datetime=datetime.now(),
        task_id='456-456'
        ).save()

    data = await weather_services.get_task_status(123)

    assert data['status'] == 'PROGRESS'
    assert data['progress'] == 0.161
    assert data['user_id'] == 123
    assert data['id'] is not None
