from src.stages.contracts.mocks.extract_contract import extract_contract_mock
from src.stages.contracts.transform_contract import TransformContract
from src.errors.transform_error import TransformError
from .transform_raw_data import TransformRawData

def test_transform():
    transform_raw_data = TransformRawData()
    transformed_data_contract = transform_raw_data.transform(extract_contract_mock)
    print(transformed_data_contract)
    assert isinstance(transformed_data_contract, TransformContract)
    assert "flight_id" in transformed_data_contract.load_content[0]
    assert "aircraft_id" in transformed_data_contract.load_content[0]
    assert "destination_id" in transformed_data_contract.load_content[0]
    assert "flight_number" in transformed_data_contract.load_content[0]
    assert "reg_number" in transformed_data_contract.load_content[0]
    assert "flag" in transformed_data_contract.load_content[0]
    assert "lat" in transformed_data_contract.load_content[0]
    assert "lng" in transformed_data_contract.load_content[0]
    assert "alt" in transformed_data_contract.load_content[0]
    assert "dir" in transformed_data_contract.load_content[0]
    assert "speed" in transformed_data_contract.load_content[0]
    assert "v_speed" in transformed_data_contract.load_content[0]
    assert "dep_icao" in transformed_data_contract.load_content[0]
    assert "dep_iata" in transformed_data_contract.load_content[0]
    assert "arr_icao" in transformed_data_contract.load_content[0]
    assert "arr_iata" in transformed_data_contract.load_content[0]
    assert "airline_icao" in transformed_data_contract.load_content[0]
    assert "airline_iata" in transformed_data_contract.load_content[0]
    assert "aircraft_icao" in transformed_data_contract.load_content[0]
    assert "updated" in transformed_data_contract.load_content[0]
    assert "status" in transformed_data_contract.load_content[0]

def test_transform_error():
    transform_raw_data = TransformRawData()

    try:
        transform_raw_data.transform('Record with eerror')
    except Exception as exception:
        assert isinstance(exception, TransformError)
