from src.stages.contracts.transform_contract import TransformContract

transform_contract_mock = TransformContract(
    load_content=[
        {
            "flight_id": "1855abaf9da2585f858e707f379a5339",
            "aircraft_id": "152002",
            "destination_id": "9f9163a3deec5ca67c4d5913ea79fd05",
            "flight_number": "1303",
            "reg_number": "RA-73730",
            "flag": "RU",
            "lat": 45.274638,
            "lng": 48.339609,
            "alt": 11099,
            "dir": 332.6,
            "speed": 837,
            "v_speed": 0,
            "dep_icao": "URMM",
            "dep_iata": "MRV",
            "arr_icao": "UUEE",
            "arr_iata": "SVO",
            "airline_icao": "AFL",
            "airline_iata": "SU",
            "aircraft_icao": "A20N",
            "updated": 1722458964,
            "status": "en-route"
        }
    ]
)
