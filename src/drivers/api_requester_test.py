from .api_requester import ApiRequester

def test_request_from_page(requests_mock):
    url = "https://airlabs.co/api/v9/flights?api_key=08741fcc-51cd-4e87-bf3a-bfcf10bfd400"
    response_context = [
        {
            "hex": "152002",
            "reg_number": "RA-73730",
            "flag": "RU",
            "lat": 45.274638,
            "lng": 48.339609,
            "alt": 11099,
            "dir": 332.6,
            "speed": 837,
            "v_speed": 0,
            "flight_number": "1303",
            "flight_icao": "AFL1303",
            "flight_iata": "SU1303",
            "dep_icao": "URMM",
            "dep_iata": "MRV",
            "arr_icao": "UUEE",
            "arr_iata": "SVO",
            "airline_icao": "AFL",
            "airline_iata": "SU",
            "aircraft_icao": "A20N",
            "updated": 1722458964,
            "status": "en-route",
            "icao24": "ABCDE"
        }
    ]
    requests_mock.get(url, status_code=200, json={"response": response_context})

    api_requester = ApiRequester("08741fcc-51cd-4e87-bf3a-bfcf10bfd400")
    request_response = api_requester.request_from_page()

    assert 'status_code' in request_response
    assert 'json' in request_response
    assert request_response["status_code"] == 200
    assert request_response["json"] == response_context
