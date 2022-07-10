from flask import Flask, render_template, request
import DB_Helper_Functions

app = Flask('__main__')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manage_reservation', methods=['GET', 'POST'])
def manage_reservation():
    if request.method == 'GET':
        return render_template('manage_reservation.html', NO_RESERVATION = False)
    elif request.method == 'POST':
        reservation_number = str(request.form.get('reservation_number'))
        reservation_name = str(request.form.get('reservation_name'))
        reservation = DB_Helper_Functions.get_db_reservation(reservation_name, reservation_number)

        if reservation['document'] is None:
            return render_template('manage_reservation.html', NO_RESERVATION = True)
        else:
            reservation=reservation['document']
            return render_template('show_reservation.html', NAME=reservation['name'],
                                   FLIGHT_CODE=reservation['flight_code'], DAY=reservation['day'],
                                   SEAT=reservation['seat'], FARE=reservation['fare_paid'],
                                   DATE_BOOKED=reservation['date_booked'],
                                   RESERVATION_NUMBER=reservation['reservation_number'])


app.run()
