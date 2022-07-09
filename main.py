import DB_Helper_Functions
from Flight_Class import Flight

# flight = Flight()
# DB_Helper_Functions.insert_flight(flight.code, flight)

flight = DB_Helper_Functions.db_load_flight('PY123')
print(flight)
print(flight.seat_map)