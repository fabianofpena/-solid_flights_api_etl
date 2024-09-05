CREATE DATABASE IF NOT EXISTS default;

USE `default`;

CREATE TABLE IF NOT EXISTS aircrafts (
    aircraft_id VARCHAR(10) PRIMARY KEY,
    reg_number VARCHAR(20),
    flag VARCHAR(10),
    aircraft_icao VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS destinations (
    destination_id CHAR(32) PRIMARY KEY,
    dep_icao VARCHAR(10),
    dep_iata VARCHAR(10),
    arr_icao VARCHAR(10),
    arr_iata VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS flights (
    flight_id CHAR(32) PRIMARY KEY,
    aircraft_id VARCHAR(10),
    destination_id CHAR(32),
    flight_number VARCHAR(20),
    airline_icao VARCHAR(10),
    airline_iata VARCHAR(10),
    status VARCHAR(20),
    updated INT,
    lat DOUBLE,
    lng DOUBLE,
    alt DOUBLE,
    dir DOUBLE,
    speed DOUBLE,
    v_speed DOUBLE,
    FOREIGN KEY (aircraft_id) REFERENCES aircrafts(aircraft_id),
    FOREIGN KEY (destination_id) REFERENCES destinations(destination_id),
    UNIQUE (aircraft_id, flight_number, updated)
);

CREATE TABLE IF NOT EXISTS aircrafts_tmp LIKE aircrafts;
CREATE TABLE IF NOT EXISTS destinations_tmp LIKE destinations;
CREATE TABLE IF NOT EXISTS flights_tmp LIKE flights;
