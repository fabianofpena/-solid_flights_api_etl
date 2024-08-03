from typing import Dict

def mock_request_from_page() -> Dict[str, str]:
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

    return {
        'status_code': 200,
        'json': {
            "response": response_context
        }
    }
