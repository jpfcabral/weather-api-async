import pytest
from mongoengine import connect, disconnect

@pytest.fixture(scope='function', autouse=True)
def mock_mongo():
    ''' Mocks mongo database '''
    connect('mongoenginetest', host='mongomock://localhost')
    yield
    disconnect()
