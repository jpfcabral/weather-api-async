import json
from typing import Dict, List


class MockResponse:
    """
    This class mocks the requests lib responses for tests purposes
    Args:
        json_data (str|list|dict): Used to retrieve and store the json response
        status_code (int): Used to set the status code response
        text (text):  Used to 
    Attributes:
        json_data (dict):
        status_code (int):
        text (text):
    """
    def __init__(
        self,
        json_data: Dict|str|List = None,
        status_code: int = 200,
        text: str = 'ok'
        ) -> None:

        if isinstance(json_data, Dict|List):
            self.json_data = json_data
        elif isinstance(json_data, str):
            with open(json_data, encoding="utf8") as json_file:
                self.json_data = json.load(json_file)
        else:
            raise ValueError('json data must be dict or (path) string')

        self.status_code = status_code
        self.text = text

    def json(self):
        ''' Return json_data attribute '''
        return self.json_data
