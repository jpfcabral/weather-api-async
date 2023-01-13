import pytest
import mongoengine as me

@pytest.fixture(scope='function', autouse=True)
def mock_mongo():
    ''' Mocks mongo database '''
    me.disconnect()
    me.connect('mongoenginetest', host='mongomock://localhost')
    yield
    me.disconnect()
