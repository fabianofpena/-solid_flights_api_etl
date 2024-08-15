import hashlib
from typing import List, Dict
from src.stages.contracts.extract_contract import ExtractContract
from src.stages.contracts.transform_contract import TransformContract
from src.errors.transform_error import TransformError

class TransformRawData:

    def transform(self, extract_contract: ExtractContract) -> TransformContract:
        try:
            transformed_information = self.__filter_and_transform_data(extract_contract)
            transformed_data_contract = TransformContract(
                load_content=transformed_information
            )
            return transformed_data_contract
        except Exception as exception:
            raise TransformError(str(exception)) from exception

    def __filter_and_transform_data(self, extract_contract: ExtractContract) -> List[Dict]:
        data_content = extract_contract.raw_information_content
        transformed_information = []

        accepted_status = {"en-route", "scheduled", "landed"}

        for data in data_content:
            if data["status"] not in accepted_status:
                # Skip this record if status is not accepted
                continue

            transformed_data = self.__transform_data(data)
            transformed_information.append(transformed_data)

        return transformed_information

    @classmethod
    def __transform_data(cls, data: Dict) -> Dict:
        aircraft_id = data["aircraft_id"]
        flight_number = data["flight_number"]
        dep_icao = data["dep_icao"]
        arr_icao = data["arr_icao"]

        # Generate unique flight_id using a hash of aircraft_id and flight_number
        flight_id = hashlib.md5(f"{aircraft_id}-{flight_number}".encode()).hexdigest()

        # Generate unique destination_id using a hash of dep_icao and arr_icao
        destination_id = hashlib.md5(f"{dep_icao}-{arr_icao}".encode()).hexdigest()
        transformed_data = {
            'flight_id': flight_id,
            'aircraft_id': aircraft_id,
            'destination_id': destination_id,
            'flight_number': flight_number,
            'reg_number': data["reg_number"],
            'flag': data["flag"],
            'lat': data["lat"],
            'lng': data["lng"],
            'alt': data["alt"],
            'dir': data["dir"],
            'speed': data["speed"],
            'v_speed': data["v_speed"],
            'dep_icao': dep_icao,
            'dep_iata': data["dep_iata"],
            'arr_icao': arr_icao,
            'arr_iata': data["arr_iata"],
            'airline_icao': data["airline_icao"],
            'airline_iata': data["airline_iata"],
            'aircraft_icao': data["aircraft_icao"],
            'updated': data["updated"],
            'status': data["status"]
        }

        return transformed_data
