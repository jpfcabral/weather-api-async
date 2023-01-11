from src.database import db


class WeatherRepository:
    ''' Weather database repository '''
    def __init__(self) -> None:
        pass

    async def insert(self, data):
        ''' Used to insert data in database '''
        doc_id = db['weather'].insert_one(data).inserted_id

        return doc_id
