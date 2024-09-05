from src.stages.contracts.mocks.transform_contract import transform_contract_mock
from src.errors.load_error import LoadError
from src.stages.load.load_data import LoadData

class RepositorySpy:
    def __init__(self) -> None:
        self.insert_flight_data_attribute = []
        self.merge_tables_called = False

    def insert_aircraft(self, data):
        pass

    def insert_destination(self, data):
        pass

    def insert_flight(self, data):
        self.insert_flight_data_attribute.append(data)

    def merge_tables(self) -> None:
        self.merge_tables_called = True

def test_load():
    repo = RepositorySpy()
    load_data = LoadData(repo)
    load_data.load(transform_contract_mock)

    assert repo.insert_flight_data_attribute[0] == transform_contract_mock.load_content[0]
    assert repo.merge_tables_called

def test_load_error():
    repo = RepositorySpy()
    load_data = LoadData(repo)

    try:
        load_data.load('Record with error')
    except Exception as exception: # pylint: disable=broad-except
        assert isinstance(exception, LoadError)
