import pickle
import Flight_Class
import requests
import json

ENDPOINT = 'https://data.mongodb-api.com/app/data-kgmzc/endpoint/data/v1'
API_KEY = 'Oqpbmxqw09Zv5GTxV1K2TUJfOhD3e1OxCi4aOzoioMbThP48Cn1OixovopqAZVHr'


def _serialize(obj):
    return pickle.dumps(obj, 0).decode()


def _deserialize(obj):
    return pickle.loads(obj.encode())


def insert_flight(flight_code: str, flight: Flight_Class.Flight):
    headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*', 'api-key': API_KEY}
    payload = {
        "dataSource": "My-Cluster",
        "database": "Airline-Reservation-System",
        "collection": "flights",
        "document": {
            'flight_code': flight_code,
            'flight_obj': _serialize(flight)
        }
    }
    r = requests.post(ENDPOINT + '/action/insertOne', headers=headers, data=json.dumps(payload))
    return r.text


def db_load_flight(flight_code: str) -> Flight_Class.Flight:
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': API_KEY
    }
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


# def db_game_update(game_id: str, updated_game: PyWordle):
#     headers = {
#         'Content-Type': 'application/json',
#         'Access-Control-Request-Headers': '*',
#         'api-key': API_KEY
#     }
#     payload = {
#         "dataSource": "My-Cluster",
#         "database": "PyWordle-API-Main",
#         "collection": "storage",
#         "filter": {
#                    "game_id": game_id
#                },
#         "update":
#             {
#             'game_id': game_id,
#             'game_obj': serialize_game(updated_game)
#             }
#     }
#     r = requests.post(ENDPOINT + '/action/updateOne', headers=headers, data=json.dumps(payload))
#     return r.json()