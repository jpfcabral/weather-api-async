from src.database import db


class WeatherRepository:
    ''' Weather database repository '''
    def __init__(self) -> None:
        pass

    def insert(self, data):
        ''' Used to insert data in database '''
        doc_id = db['weather'].insert_one(data).inserted_id

        return doc_id

    def read_by_user_id(self, user_id):
        ''' Get a document from database by user_id field'''
        doc = db['weather'].find_one({'user_id': user_id})

        doc['id'] = str(doc['_id'])
        del doc['_id']
        return doc
