import pytest
from pathlib import Path
from tests.mocks.mocker_response import MockResponse
from src.weather.tasks import request_weather_data

def test_request_weather_data(mocker):
    mocker.patch(
        'src.weather.tasks.requests.post',
        return_value=MockResponse(json_data=str(Path('tests/mocks/open_weather_api_response.json')))
    )
    mocker.patch(
        'src.weather.tasks.request_weather_data.update_state',
        return_value=None
    )
    mocker.patch(
        'src.weather.tasks.weather_repository.insert_weather_data',
        return_value=None
    )

    request_weather_data(user_id=123, req_delay=0.001)
