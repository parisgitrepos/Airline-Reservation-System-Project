import requests
import json
import random
import os
import Flight_Class


ENDPOINT = 'https://data.mongodb-api.com/app/data-kgmzc/endpoint/data/v1'

# Check whether local computer has config (declared in .gitignore) otherwise assume deployment stage and get from env
file_exists = os.path.isfile(os.path.abspath('config.py'))
if file_exists:
    import config
    API_KEY = config.API_KEY
else:
    API_KEY = os.getenv('API_KEY')

GENERIC_HEADERS = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*', 'api-key': API_KEY}


def db_insert_flight(code='PY123', from_airport='LAX', to_airport='JFK', time='17:00', duration=4.5, fare=100.99,
                     day='Friday', seat_map_name='PERSONAL JET'):
    seat_map = db_get_seat_map(seat_map_name)
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
            'seat_map_name': seat_map_name,
            'seat_map': seat_map,
            'duration': duration,
            'fare': fare,
        }
    }
    r = requests.post(ENDPOINT + '/action/insertOne', headers=GENERIC_HEADERS, data=json.dumps(payload))
    return r.status_code


def db_load_flight(code: str, day: str, time:str):
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
    r = requests.post(ENDPOINT + '/action/findOne', headers=GENERIC_HEADERS, data=json.dumps(payload))
    return r.json()['document']


def db_generate_reservation(name, flight_code, day, time, seat, fare_paid, date_booked):
    name = name.upper()
    reservation_number = ''.join((str(random.randint(0, 9)) for digits in range(10)))
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "reservations",
        "document": {
            'name': name,
            'flight_code': flight_code,
            'day': day,
            'time': time,
            'seat': seat,
            'fare_paid': fare_paid,
            'date_booked': date_booked,
            'reservation_number': reservation_number
        }
    }
    requests.post(ENDPOINT + '/action/insertOne', headers=GENERIC_HEADERS, data=json.dumps(payload))
    return reservation_number


def db_get_reservation(name, reservation_number):
    name = name.upper()
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
    r = requests.post(ENDPOINT + '/action/findOne', headers=GENERIC_HEADERS, data=json.dumps(payload))
    return r.json()


def db_generate_seat_map(name, rows, seats_per_row: int):
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
    r = requests.post(ENDPOINT + '/action/insertOne', headers=GENERIC_HEADERS, data=json.dumps(payload))
    return r.status_code


def db_get_seat_map(name):
    name = name.upper()
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "seat_maps",
        "filter":
            {
                "name": name,
            }
    }
    r = requests.post(ENDPOINT + '/action/findOne', headers=GENERIC_HEADERS, data=json.dumps(payload))
    return r.json()['document']


def db_get_available_seat_maps():
    available_seat_maps = []
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "seat_maps",
    }

    r = requests.post(ENDPOINT + '/action/find', headers=GENERIC_HEADERS, data=json.dumps(payload))

    for seat_map in r.json()['documents']:
        available_seat_maps.append(seat_map['name'])

    return available_seat_maps


def db_update_flight(flight_obj):
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


def db_find_flights(from_airport, to_airport, day):
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "flights",
        "filter":
            {
                "from": from_airport,
                "to": to_airport,
                "day": day
            }
    }

    r = requests.post(ENDPOINT + '/action/find', headers=GENERIC_HEADERS, data=json.dumps(payload))
    flight_options = []
    for flight in r.json()['documents']:
        flight_options.append([flight['code'], flight['day'], flight['time']])

    return flight_options


def db_reservation_exists(name, reservation_number):
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "reservations",
        "filter":
            {
                "name": name,
                "reservation_number": reservation_number
            }
    }

    r = requests.post(ENDPOINT + '/action/find', headers=GENERIC_HEADERS, data=json.dumps(payload))

    if len(r.json()['documents']) == 0:
        return False
    else:
        return True


def db_cancel_reservation(name, reservation_number):
    if not db_reservation_exists(name, reservation_number):
        return 'No reservation found!'
    else:
        payload = {
            "dataSource": "My-Cluster",
            "database": "Airline-Reservation-System",
            "collection": "reservations",
            "filter": {
                'name': name,
                'reservation_number': reservation_number
            },
            "update": {
                "$set": {
                    'seat': 'CANCELLED'
                    }
                }
            }

        requests.post(ENDPOINT + '/action/updateOne', headers=GENERIC_HEADERS, data=json.dumps(payload))

        return 'Success!'


def db_reservation_change_seat(name, reservation_number, new_seat):
    if not db_reservation_exists(name, reservation_number):
        return 'No reservation found!'
    else:
        payload = {
            "dataSource": "My-Cluster",
            "database": "Airline-Reservation-System",
            "collection": "reservations",
            "filter": {
                'name': name,
                'reservation_number': reservation_number
            },
            "update": {
                "$set": {
                    'seat': new_seat
                    }
                }
            }

        requests.post(ENDPOINT + '/action/updateOne', headers=GENERIC_HEADERS, data=json.dumps(payload))

        return 'Success!'
