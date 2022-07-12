from flask import Flask, render_template, request
import DB_Helper_Functions
from Flight_Class import Flight

app = Flask('__main__')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/manage_reservation', methods=['GET', 'POST'])
def manage_reservation():
    if request.method == 'GET':
        return render_template('manage_reservation_page.html', NO_RESERVATION=False)
    elif request.method == 'POST':
        reservation_number = str(request.form.get('reservation_number'))
        reservation_name = str(request.form.get('reservation_name'))
        reservation = DB_Helper_Functions.get_db_reservation(reservation_name, reservation_number)

        if reservation['document'] is None:
            return render_template('manage_reservation_page.html', NO_RESERVATION=True)
        else:
            reservation = reservation['document']
            return render_template('show_reservation.html', NAME=reservation['name'],
                                   FLIGHT_CODE=reservation['flight_code'], DAY=reservation['day'],
                                   SEAT=reservation['seat'], FARE=reservation['fare_paid'],
                                   DATE_BOOKED=reservation['date_booked'],
                                   RESERVATION_NUMBER=reservation['reservation_number'])


@app.route('/admin_selector')
def admin_selector():
    return render_template('admin_select.html')


@app.route('/super_admin', methods=['GET', 'POST'])
def super_admin():
    if request.method == 'GET':
        return render_template('super_admin.html', HIDE_INCORRECT_PASSWORD=True)
    elif request.method == 'POST':
        if request.form.get('form') == 'password':
            if str(request.form.get('password')) == 'APTIV':
                return render_template('super_admin_panel.html',
                                       SEAT_MAPS=DB_Helper_Functions.get_db_available_seat_maps())
            else:
                return render_template('super_admin.html', HIDE_INCORRECT_PASSWORD=False)
        elif request.form.get('form') == 'seat_map_form':
            aircraft = request.form.get('aircraft')
            num_rows = request.form.get('rows')
            seats_per_row = request.form.get('seats_per_row')

            status_code = DB_Helper_Functions.generate_db_seat_map(aircraft, int(num_rows), int(seats_per_row))

            return render_template('super_admin_panel.html',
                                   SEAT_MAP_RESPONSE='Success!' if status_code == 201 else 'Error!')
        elif request.form.get('form') == 'new_flight_form':
            from_airport = request.form.get('from')
            to_airport = request.form.get('to')
            duration = request.form.get('duration')
            fare = request.form.get('fare')
            code = request.form.get('code')
            time = request.form.get('time')
            day = request.form.get('day')
            seat_map = request.form.get('seat_map')

            status_code = DB_Helper_Functions.insert_flight(code, from_airport, to_airport, time, duration, fare, day,
                                                            seat_map)

            return render_template('super_admin_panel.html',
                                   NEW_FLIGHT_RESPONSE='Success!' if status_code == 201 else 'Error!')


app.run()
