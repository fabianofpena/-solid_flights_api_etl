# pylint: disable=W0221, W1203
from typing import List, Dict
from .interfaces.api_collector import ApiCollectorInterface

class ApiCollector(ApiCollectorInterface):
    REQUIRED_KEYS = {
        "hex", "flight_number", "reg_number", "flag", "lat", "lng", "alt", "dir", "speed",
        "v_speed", "dep_icao", "dep_iata", "arr_icao", "arr_iata", "airline_icao",
        "airline_iata", "aircraft_icao", "updated", "status"
    }

    def collect_essential_information(self, json_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        if not isinstance(json_data, list):
            raise ValueError(f"Unexpected response format: Expected a list. Response: {json_data}")

        extracted_data = []
        for flight in json_data:
            if not all(key in flight for key in self.REQUIRED_KEYS):
                continue

            extracted_data.append({
                'aircraft_id': flight["hex"],
                'flight_number': flight["flight_number"],
                'reg_number': flight["reg_number"],
                'flag': flight["flag"],
                'lat': flight["lat"],
                'lng': flight["lng"],
                'alt': flight["alt"],
                'dir': flight["dir"],
                'speed': flight["speed"],
                'v_speed': flight["v_speed"],
                'dep_icao': flight["dep_icao"],
                'dep_iata': flight["dep_iata"],
                'arr_icao': flight["arr_icao"],
                'arr_iata': flight["arr_iata"],
                'airline_icao': flight["airline_icao"],
                'airline_iata': flight["airline_iata"],
                'aircraft_icao': flight["aircraft_icao"],
                'updated': flight["updated"],
                'status': flight["status"]
            })

        return extracted_data
