import DB_Helper_Functions

class Flight:
    def __init__(self, code='PY123', from_airport='LAX', to_airport='JFK', time='17:00', duration = 4.5,
                 days_operating=None, seat_map=None, seat_arrangement=None):

        # Setting default value for days_operating like this to comply with PyCharm recommended syntax
        if days_operating is None:
            self.days_operating = ['Sunday', 'Monday', 'Friday']
        else:
            self.days_operating = days_operating
        # Dict similar to {'1A': {'booked': False}, '1B': {'booked': False}, '1C': {'booked': False},
        #                   '1D': {'booked': False}, '2A': {'booked': False}, ...}
        if seat_map is None:
            self.seat_map = {}
            for row in range(30):
                for col in range(4):
                    if col == 0:
                        seat = str(row) + 'A'
                    elif col == 1:
                        seat = str(row) + 'B'
                    elif col == 2:
                        seat = str(row) + 'C'
                    elif col == 3:
                        seat = str(row) + 'D'
                    else:
                        seat = 'Error'

                    self.seat_map[seat] = {'booked': False}
        else:
            self.seat_map = seat_map

        # NOTE - Assume only 2 columns
        if seat_arrangement is None:
            self.seat_arrangement = {'seats_per_row': 4, 'seats_per_col': 2}
        else:
            self.seat_arrangement = seat_arrangement

        self.code = code
        self.from_airport = from_airport
        self.to_airport = to_airport
        self.time = time
        self.duration = duration

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

    def formatted_seat_map(self):
        seat_codes = list(self.seat_map.keys())
        seats_per_row = self.seat_arrangement['seats_per_row']
        seats_per_col = self.seat_arrangement['seats_per_col']

        seat_codes = zip(*(seat_codes[i:] for i in range(seats_per_row)))
        seat_codes = list(seat_codes)[::seats_per_row]
        seat_codes_first_col = []
        seat_codes_second_col = []

        for row in seat_codes:
            seat_codes_first_col.append(row[:int(len(row)/2)])

        for row in seat_codes:
            seat_codes_second_col.append(row[int(len(row)/2):])

        return {'row1': seat_codes_first_col, 'row2': seat_codes_second_col}

    def reset(self):
        for seat in list(self.seat_map.keys()):
            self.cancel_seat(seat)

