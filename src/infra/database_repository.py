from typing import Dict
from src.infra.database_connector import DatabaseConnection

class DatabaseRepositoryInterface:
    def insert_aircraft(self, data: Dict) -> None:
        raise NotImplementedError

    def insert_destination(self, data: Dict) -> None:
        raise NotImplementedError

    def insert_flight(self, data: Dict) -> None:
        raise NotImplementedError

    def merge_tables(self) -> None:
        raise NotImplementedError

class DatabaseRepository(DatabaseRepositoryInterface):
    @classmethod
    def insert_aircraft(cls, data: Dict) -> None:
        query = '''
            INSERT INTO aircrafts_tmp (aircraft_id, reg_number, flag, aircraft_icao)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                reg_number = VALUES(reg_number),
                flag = VALUES(flag),
                aircraft_icao = VALUES(aircraft_icao)
        '''
        cursor = DatabaseConnection.connection.cursor()
        cursor.execute(query, (data['aircraft_id'], data['reg_number'], data['flag'], data['aircraft_icao']))
        DatabaseConnection.connection.commit()

    @classmethod
    def insert_destination(cls, data: Dict) -> None:
        query = '''
            INSERT INTO destinations_tmp (destination_id, dep_icao, dep_iata, arr_icao, arr_iata)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                dep_icao = VALUES(dep_icao),
                dep_iata = VALUES(dep_iata),
                arr_icao = VALUES(arr_icao),
                arr_iata = VALUES(arr_iata)
        '''
        cursor = DatabaseConnection.connection.cursor()
        cursor.execute(query, (data['destination_id'], data['dep_icao'], data['dep_iata'], data['arr_icao'], data['arr_iata']))
        DatabaseConnection.connection.commit()

    @classmethod
    def insert_flight(cls, data: Dict) -> None:
        query = '''
            INSERT INTO flights_tmp (flight_id, aircraft_id, destination_id, flight_number, airline_icao, airline_iata, status, updated, lat, lng, alt, dir, speed, v_speed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                airline_icao = VALUES(airline_icao),
                airline_iata = VALUES(airline_iata),
                status = VALUES(status),
                updated = VALUES(updated),
                lat = VALUES(lat),
                lng = VALUES(lng),
                alt = VALUES(alt),
                dir = VALUES(dir),
                speed = VALUES(speed),
                v_speed = VALUES(v_speed),
                aircraft_id = VALUES(aircraft_id),
                destination_id = VALUES(destination_id)
        '''
        cursor = DatabaseConnection.connection.cursor()
        cursor.execute(query, (
            data['flight_id'], data['aircraft_id'], data['destination_id'], data['flight_number'], 
            data['airline_icao'], data['airline_iata'], data['status'], data['updated'], 
            data['lat'], data['lng'], data['alt'], data['dir'], data['speed'], data['v_speed']
        ))
        DatabaseConnection.connection.commit()

    @classmethod
    def merge_tables(cls) -> None:
        merge_queries = [
            '''
            INSERT INTO aircrafts (aircraft_id, reg_number, flag, aircraft_icao)
            SELECT aircraft_id, reg_number, flag, aircraft_icao FROM aircrafts_tmp
            ON DUPLICATE KEY UPDATE
                reg_number = VALUES(reg_number),
                flag = VALUES(flag),
                aircraft_icao = VALUES(aircraft_icao)
            ''',
            '''
            INSERT INTO destinations (destination_id, dep_icao, dep_iata, arr_icao, arr_iata)
            SELECT destination_id, dep_icao, dep_iata, arr_icao, arr_iata FROM destinations_tmp
            ON DUPLICATE KEY UPDATE
                dep_icao = VALUES(dep_icao),
                dep_iata = VALUES(dep_iata),
                arr_icao = VALUES(arr_icao),
                arr_iata = VALUES(arr_iata)
            ''',
            '''
            INSERT INTO flights (flight_id, aircraft_id, destination_id, flight_number, airline_icao, airline_iata, status, updated, lat, lng, alt, dir, speed, v_speed)
            SELECT flight_id, aircraft_id, destination_id, flight_number, airline_icao, airline_iata, status, updated, lat, lng, alt, dir, speed, v_speed FROM flights_tmp
            ON DUPLICATE KEY UPDATE
                airline_icao = VALUES(airline_icao),
                airline_iata = VALUES(airline_iata),
                status = VALUES(status),
                updated = VALUES(updated),
                lat = VALUES(lat),
                lng = VALUES(lng),
                alt = VALUES(alt),
                dir = VALUES(dir),
                speed = VALUES(speed),
                v_speed = VALUES(v_speed),
                aircraft_id = VALUES(aircraft_id),
                destination_id = VALUES(destination_id)
            '''
        ]
        cursor = DatabaseConnection.connection.cursor()
        for query in merge_queries:
            cursor.execute(query)
        DatabaseConnection.connection.commit()
