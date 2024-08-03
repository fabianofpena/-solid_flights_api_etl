from typing import Dict
import requests
from .interfaces.api_requester import ApiRequesterInterface

class ApiRequester(ApiRequesterInterface):

    def __init__(self, api_key: str, timeout: int = 10) -> None:
        self.__url = "https://airlabs.co/api/v9/flights"
        self.__api_key = api_key
        self.__timeout = timeout

    def request_from_page(self) -> Dict[int, str]:
        response = requests.get(f"{self.__url}?api_key={self.__api_key}", timeout=self.__timeout)
        response_json = response.json()
        return {
            "status_code": response.status_code,
            "json": response_json.get("response", [])
        }
