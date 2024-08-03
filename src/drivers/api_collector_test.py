from .mocks.api_requester_mock import mock_request_from_page
from .api_collector import ApiCollector

def test_collect_essential_information():
    http_request_response = mock_request_from_page()

    json_data = http_request_response['json']['response']

    extracted_data = ApiCollector.collect_essential_information(json_data)

    assert isinstance(extracted_data, list)
    assert isinstance(extracted_data[0], dict)
    assert 'aircraft_id' in extracted_data[0]
    assert 'flight_number' in extracted_data[0]
    assert 'reg_number' in extracted_data[0]
    assert 'flag' in extracted_data[0]
    assert 'lat' in extracted_data[0]
    assert 'lng' in extracted_data[0]
    assert 'alt' in extracted_data[0]
    assert 'dir' in extracted_data[0]
    assert 'speed' in extracted_data[0]
    assert 'v_speed' in extracted_data[0]
    assert 'dep_icao' in extracted_data[0]
    assert 'dep_iata' in extracted_data[0]
    assert 'arr_icao' in extracted_data[0]
    assert 'arr_iata' in extracted_data[0]
    assert 'airline_icao' in extracted_data[0]
    assert 'airline_iata' in extracted_data[0]
    assert 'aircraft_icao' in extracted_data[0]
    assert 'updated' in extracted_data[0]
    assert 'status' in extracted_data[0]
