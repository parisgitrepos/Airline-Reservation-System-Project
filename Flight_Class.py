import DB_Helper_Functions


class Flight:
    def __init__(self, code='PY123', day='Friday', time='17:00'):

        flight_info = DB_Helper_Functions.db_load_flight(code, day, time)
        self.code = flight_info['code']
        self.from_airport = flight_info['from']
        self.to_airport = flight_info['to']
        self.time = flight_info['time']
        self.duration = flight_info['duration']
        self.day_operating = flight_info['day']
        self.fare = flight_info['fare']

        self.seat_map_info = flight_info['seat_map']
        self.seat_map = self.seat_map_info['seat_map']
        self.seat_arrangement = self.seat_map_info['seat_arrangement']

    def _seat_available(self, seat_code):
        return True if self.seat_map[seat_code]['booked'] is False else False

    def reserve_seat(self, seat_code, name, reservation_number):
        if self._seat_available(seat_code) is True:
            self.seat_map[seat_code] = {'booked': True, 'name': name, 'reservation_number': reservation_number}
            return True
        else:
            return False

    def cancel_seat(self, seat_code='1A'):
        self.seat_map[seat_code] = {'booked': False}

    def get_available_seats(self):
        available_seats = []
        for seat_code in list(self.seat_map.keys()):
            if self.seat_map[seat_code]['booked'] is False:
                available_seats.append(seat_code)

        return available_seats

    def get_seat_map(self):
        seat_codes = list(self.seat_map.keys())
        seats_per_row = self.seat_arrangement['seats_per_row']

        seat_codes = zip(*(seat_codes[i:] for i in range(seats_per_row)))
        seat_codes = list(seat_codes)[::seats_per_row]
        seat_codes_first_col = []
        seat_codes_second_col = []

        for row in seat_codes:
            seat_codes_first_col.append(row[:int(len(row) / 2)])

        for row in seat_codes:
            seat_codes_second_col.append(row[int(len(row) / 2):])

        return {'col1': seat_codes_first_col, 'col2': seat_codes_second_col}

    def get_fare(self):
        return self.fare

    def reset(self):
        for seat in list(self.seat_map.keys()):
            self.cancel_seat(seat)

    def db_sync(self):
        DB_Helper_Functions.update_db_flight(self)
