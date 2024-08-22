from abc import ABC, abstractmethod
from typing import Dict

class DatabaseRepositoryInterface(ABC):

    @abstractmethod
    def insert_aircraft(self, data: Dict) -> None:
        pass

    @abstractmethod
    def insert_destination(self, data: Dict) -> None:
        pass

    @abstractmethod
    def insert_flight(self, data: Dict) -> None:
        pass

    @abstractmethod
    def merge_tables(self) -> None:
        pass