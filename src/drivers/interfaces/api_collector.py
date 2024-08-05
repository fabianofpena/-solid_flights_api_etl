from abc import ABC, abstractmethod
from typing import List, Dict

class ApiCollectorInterface(ABC):

    @abstractmethod
    def collect_essential_information(self, json_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        pass
