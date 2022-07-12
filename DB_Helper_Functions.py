import pickle
import requests
import json
import random


ENDPOINT = 'https://data.mongodb-api.com/app/data-kgmzc/endpoint/data/v1'
API_KEY = 'Oqpbmxqw09Zv5GTxV1K2TUJfOhD3e1OxCi4aOzoioMbThP48Cn1OixovopqAZVHr'
GENERIC_HEADERS = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*', 'api-key': API_KEY}


def insert_flight(code='PY123', from_airport='LAX', to_airport='JFK', time='17:00', duration=4.5, fare=100.99,
                  day='Friday', seat_map_name='PERSONAL_JET'):
    seat_map = get_db_seat_map(seat_map_name)
    headers = GENERIC_HEADERS
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "flights",
        "document": {
            'code': code,
            'from': from_airport,
            'to': to_airport,
            'time': time,
            'day': day,
            'seat_map': seat_map,
            'duration': duration,
            'fare': fare,
        }
    }
    r = requests.post(ENDPOINT + '/action/insertOne', headers=headers, data=json.dumps(payload))
    return r.status_code


def db_load_flight(code: str, day: str, time:str):
    headers = GENERIC_HEADERS
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "flights",
        "filter":
            {
                "code": code,
                "day": day,
                "time": time
            }
    }
    r = requests.post(ENDPOINT + '/action/findOne', headers=headers, data=json.dumps(payload))
    return r.json()['document']


def generate_db_reservation(name, flight_code, day, seat, fare_paid, date_booked):
    name = name.upper()
    reservation_number = ''.join((str(random.randint(0, 9)) for digits in range(10)))
    headers = GENERIC_HEADERS
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "reservations",
        "document": {
            'name': name,
            'flight_code': flight_code,
            'day': day,
            'seat': seat,
            'fare_paid': fare_paid,
            'date_booked': date_booked,
            'reservation_number': reservation_number
        }
    }
    requests.post(ENDPOINT + '/action/insertOne', headers=headers, data=json.dumps(payload))
    return reservation_number


def get_db_reservation(name, reservation_number):
    name = name.upper()
    headers = GENERIC_HEADERS
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "reservations",
        "filter":
            {
                "name": name,
                'reservation_number': reservation_number
            }
    }
    r = requests.post(ENDPOINT + '/action/findOne', headers=headers, data=json.dumps(payload))
    return r.json()


def generate_db_seat_map(name, rows, seats_per_row: int):
    if seats_per_row > 6:
        return 'Error'

    if seats_per_row % 2 != 0:
        return 'Error'

    seat_map = {}
    for row in range(1, rows + 1):
        for col in range(seats_per_row):
            if col == 0:
                seat = str(row) + 'A'
            elif col == 1:
                seat = str(row) + 'B'
            elif col == 2:
                seat = str(row) + 'C'
            elif col == 3:
                seat = str(row) + 'D'
            elif col == 4:
                seat = str(row) + 'E'
            elif col == 5:
                seat = str(row) + 'F'
            else:
                seat = 'ERROR'
            seat_map[seat] = {'booked': False}

    name = name.upper()
    headers = GENERIC_HEADERS
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "seat_maps",
        "document":
            {
                "name": name,
                'seat_arrangement': {'seats_per_row': seats_per_row, 'seats_per_col': seats_per_row / 2, 'num_cols': 2},
                'seat_map': seat_map
            }
    }
    r = requests.post(ENDPOINT + '/action/insertOne', headers=headers, data=json.dumps(payload))
    return r.status_code


def get_db_seat_map(name):
    name = name.upper()
    headers = GENERIC_HEADERS
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "seat_maps",
        "filter":
            {
                "name": name,
            }
    }
    r = requests.post(ENDPOINT + '/action/findOne', headers=headers, data=json.dumps(payload))
    return r.json()['document']


def get_db_available_seat_maps():
    available_seat_maps = []
    headers = GENERIC_HEADERS
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "seat_maps",
    }

    r = requests.post(ENDPOINT + '/action/find', headers=headers, data=json.dumps(payload))

    for seat_map in r.json()['documents']:
        available_seat_maps.append(seat_map['name'])

    return available_seat_maps


def update_db_flight(flight_obj):
    flight_obj = flight_obj
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "flights",
        "filter": {
            'code': flight_obj.code,
            'day': flight_obj.day_operating,
            'time': flight_obj.time
        },
        "update": {
            "$set": {
                'code': flight_obj.code,
                'from': flight_obj.from_airport,
                'to': flight_obj.to_airport,
                'time': flight_obj.time,
                'day': flight_obj.day_operating,
                'seat_map': {
                    'seat_arrangement': flight_obj.seat_arrangement,
                    'seat_map': flight_obj.seat_map
                },
                'duration': flight_obj.duration,
                'fare': flight_obj.fare
            }
        }
    }

    r = requests.post(ENDPOINT + '/action/updateOne', headers=GENERIC_HEADERS, data=json.dumps(payload))
    return r.status_code
