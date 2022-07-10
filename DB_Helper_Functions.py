import pickle
import Flight_Class
import requests
import json
import random

ENDPOINT = 'https://data.mongodb-api.com/app/data-kgmzc/endpoint/data/v1'
API_KEY = 'Oqpbmxqw09Zv5GTxV1K2TUJfOhD3e1OxCi4aOzoioMbThP48Cn1OixovopqAZVHr'
GENERIC_HEADERS = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*', 'api-key': API_KEY}


def _serialize(obj):
    return pickle.dumps(obj, 0).decode()


def _deserialize(obj):
    return pickle.loads(obj.encode())


def insert_flight(flight_code: str, flight_time:str, flight_from: str, flight_to: str, day_operating: str,
                  flight: Flight_Class.Flight):
    headers = GENERIC_HEADERS
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "flights",
        "document": {
            'flight_code': flight_code,
            'flight_from': flight_from,
            'flight_to': flight_to,
            'flight_time': flight_time,
            'day_operating': day_operating,
            'flight_obj': _serialize(flight)
        }
    }
    r = requests.post(ENDPOINT + '/action/insertOne', headers=headers, data=json.dumps(payload))
    return r.text


def db_load_flight(flight_code: str) -> Flight_Class.Flight:
    headers = GENERIC_HEADERS
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "flights",
        "filter":
            {
                "flight_code": flight_code
            }
    }
    r = requests.post(ENDPOINT + '/action/findOne', headers=headers, data=json.dumps(payload))
    return _deserialize(r.json()['document']['flight_obj'])


def create_db_reservation(name, flight_code, day, seat, fare_paid, date_booked):
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
