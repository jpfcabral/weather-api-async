from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_collect_weather_data(mocker):
    mocker.patch(
        'src.weather.routers.WeatherServices.collect_weather_data_and_save',
        return_value={
            "user_id": 456,
            "request_datetime": "2023-01-12T00:00:00",
            "task_id": "dd53e8a9-ae4f-45fa-917e-a048caf8f59f",
            "weather_data": [],
            "id": "63c01ef9c608c660566fdd15"
        }
    )

    response = client.post('/weather/', params={'user_id': '123'})

    assert response.status_code == 200

def test_collect_weather_data_no_provided_user_id(mocker):
    mocker.patch(
        'src.weather.routers.WeatherServices.collect_weather_data_and_save',
        return_value={
            "user_id": 456,
            "request_datetime": "2023-01-12T00:00:00",
            "task_id": "dd53e8a9-ae4f-45fa-917e-a048caf8f59f",
            "weather_data": [],
            "id": "63c01ef9c608c660566fdd15"
        }
    )

    response = client.post('/weather/')

    assert response.status_code == 422
