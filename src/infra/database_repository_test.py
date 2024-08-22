import re
from unittest.mock import patch, MagicMock
import pytest
from src.infra.database_repository import DatabaseRepository
from src.infra.database_connector import DatabaseConnection
from src.stages.contracts.mocks.transform_contract import transform_contract_mock

def normalize_sql(sql):
    """Normalize SQL string by stripping leading/trailing whitespaces and reducing multiple spaces to a single space."""
    return re.sub(r'\s+', ' ', sql.strip())

@pytest.fixture(autouse=True)
def setup_database():
    with patch('src.infra.database_repository.DatabaseConnection') as mock_db_conn:
        mock_cursor = MagicMock()
        mock_db_conn.connection.cursor.return_value = mock_cursor
        DatabaseConnection.connect()
        yield mock_db_conn, mock_cursor

def test_insert_aircraft(setup_database):
    mock_db_conn, mock_cursor = setup_database

    data = transform_contract_mock.load_content[0]

    DatabaseRepository.insert_aircraft(data)

    expected_sql = '''
        INSERT INTO aircrafts_tmp (aircraft_id, reg_number, flag, aircraft_icao)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            reg_number = VALUES(reg_number),
            flag = VALUES(flag),
            aircraft_icao = VALUES(aircraft_icao)
    '''
    actual_sql = mock_cursor.execute.call_args[0][0]

    assert normalize_sql(expected_sql) == normalize_sql(actual_sql)
    assert mock_cursor.execute.call_args[0][1] == (
        data['aircraft_id'], data['reg_number'], data['flag'], data['aircraft_icao']
    )
    mock_db_conn.connection.commit.assert_called_once()

def test_insert_destination(setup_database):
    mock_db_conn, mock_cursor = setup_database

    data = transform_contract_mock.load_content[0]

    DatabaseRepository.insert_destination(data)

    expected_sql = '''
        INSERT INTO destinations_tmp (destination_id, dep_icao, dep_iata, arr_icao, arr_iata)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            dep_icao = VALUES(dep_icao),
            dep_iata = VALUES(dep_iata),
            arr_icao = VALUES(arr_icao),
            arr_iata = VALUES(arr_iata)
    '''
    actual_sql = mock_cursor.execute.call_args[0][0]

    assert normalize_sql(expected_sql) == normalize_sql(actual_sql)
    assert mock_cursor.execute.call_args[0][1] == (
        data['destination_id'], data['dep_icao'], data['dep_iata'], data['arr_icao'], data['arr_iata']
    )
    mock_db_conn.connection.commit.assert_called_once()

def test_insert_flight(setup_database):
    mock_db_conn, mock_cursor = setup_database

    data = transform_contract_mock.load_content[0]

    DatabaseRepository.insert_flight(data)

    expected_sql = '''
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
    actual_sql = mock_cursor.execute.call_args[0][0]

    assert normalize_sql(expected_sql) == normalize_sql(actual_sql)
    assert mock_cursor.execute.call_args[0][1] == (
        data['flight_id'], data['aircraft_id'], data['destination_id'], data['flight_number'],
        data['airline_icao'], data['airline_iata'], data['status'], data['updated'],
        data['lat'], data['lng'], data['alt'], data['dir'], data['speed'], data['v_speed']
    )
    mock_db_conn.connection.commit.assert_called_once()

def test_merge_tables(setup_database):
    mock_db_conn, mock_cursor = setup_database

    DatabaseRepository.merge_tables()

    assert mock_cursor.execute.call_count == 3
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
    for expected_sql in merge_queries:
        assert any(normalize_sql(expected_sql) == normalize_sql(call_args[0][0]) for call_args in mock_cursor.execute.call_args_list)
    mock_db_conn.connection.commit.assert_called_once()
