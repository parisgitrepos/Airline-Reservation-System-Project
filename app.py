import flask
from flask import Flask, render_template, request
import DB_Helper_Functions
from Flight_Class import Flight
import datetime
from zoneinfo import ZoneInfo

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
        reservation = DB_Helper_Functions.db_get_reservation(reservation_name, reservation_number)

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
        return render_template('super_admin_login.html', HIDE_INCORRECT_PASSWORD=True)
    elif request.method == 'POST':
        if request.form.get('form') == 'password':
            if str(request.form.get('password')) == 'APTIV':
                return render_template('super_admin_panel.html',
                                       SEAT_MAPS=DB_Helper_Functions.db_get_available_seat_maps())
            else:
                return render_template('super_admin_login.html', HIDE_INCORRECT_PASSWORD=False)
        elif request.form.get('form') == 'seat_map_form':
            aircraft = request.form.get('aircraft')
            num_rows = request.form.get('rows')
            seats_per_row = request.form.get('seats_per_row')

            status_code = DB_Helper_Functions.db_generate_seat_map(aircraft, int(num_rows), int(seats_per_row))

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

            status_code = DB_Helper_Functions.db_insert_flight(code, from_airport, to_airport, time, duration, fare,
                                                               day,
                                                               seat_map)

            return render_template('super_admin_panel.html',
                                   NEW_FLIGHT_RESPONSE='Success!' if status_code == 201 else 'Error!')


@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'GET':
        date_min = datetime.datetime.now(ZoneInfo('US/Eastern')).strftime('%Y-%m-%d')
        date_max = (datetime.datetime.now(ZoneInfo('US/Eastern')) + datetime.timedelta(days=6)).strftime('%Y-%m-%d')

        if 'ref' in list(request.args.keys()):
            if request.args.get('ref') == 'NoFlights':
                return render_template('new_booking_query.html', DATE_MIN=date_min, DATE_MAX=date_max, NO_FLIGHTS=True)
        else:
            return render_template('new_booking_query.html', DATE_MIN=date_min, DATE_MAX=date_max, NO_FLIGHTS=False)
    elif request.method == 'POST':
        code = request.form.get('code')
        day = request.form.get('day')
        time = request.form.get('time')
        return 'WIP'


@app.route('/flight_finder')
def flight_finder():
    if len(list(request.args.keys())) == 0:
        return flask.redirect('/book')
    else:
        flight_date = request.args.get('date')
        from_airport = request.args.get('from_airport')
        to_airport = request.args.get('to_airport')

        flight_date = datetime.datetime(year=int(flight_date[0:4]),
                                        month=int(flight_date[5:7]), day=int(flight_date[8:10]))
        flight_date = flight_date.weekday()

        if flight_date == 0:
            flight_date = 'Monday'
        elif flight_date == 1:
            flight_date = 'Tuesday'
        elif flight_date == 2:
            flight_date = 'Wednesday'
        elif flight_date == 3:
            flight_date = 'Thursday'
        elif flight_date == 4:
            flight_date = 'Friday'
        elif flight_date == 5:
            flight_date = 'Saturday'
        elif flight_date == 6:
            flight_date = 'Sunday'

        flight_info = DB_Helper_Functions.db_find_flights(from_airport, to_airport, flight_date)

        if len(flight_info) == 0:
            return flask.redirect('/book?ref=NoFlights')
        else:
            flight_objs = [Flight(flight[0], flight[1], flight[2]) for flight in flight_info]
            flight_objs_attrs = []

            for flight in flight_objs:
                flight_objs_attrs.append({'code': flight.code, 'from_airport': flight.from_airport,
                                          'to_airport': flight.to_airport, 'duration': flight.duration,
                                          'time': flight.time, 'day': flight.day_operating, 'fare': flight.fare,
                                          'sold_out': True if flight.get_available_seats() == [] else False})

            return render_template('show_flight_options.html', FLIGHT_OPTIONS_LIST=flight_objs_attrs)


app.run()
