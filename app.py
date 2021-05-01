### REQUIREMENTS ### (delete when complete)
# 5. home page should deal with error message and link to other interfaces
# 6. general use cases: ViewMyFlights, SearchFlights, Logout
# 7. Customer: PurchaseTickets, TrackMySpending
# 8. BookingAgent: PurchaseTickets, ViewMyCommission, ViewTopCustomers
# 9. AirlineStaff: CreateNewFlights, ChangeFlightStatus, AddAirplane, AddAirport, 
#           ViewBookingAgents, ViewReports, RevenueComparison, ViewTopDestinations
# 10. enforce constraints: e.g. customer can't create new flights

# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import mysql.connector
import hashlib
from datetime import datetime, date


# Initialize the app from Flask (and reference templates!)
app = Flask(__name__,
            static_url_path="/",
            static_folder="static")


# Configure MySQL
conn = mysql.connector.connect(host='localhost',
                               user='root',
                               password='password',  # comment out this line if not needed
                               database='air',
                               port=3306)


# Define route for login
@app.route('/')
def index():
    return render_template('login.html')


# --------- prevent SQL injection --------
def check_injection(string_input):
	assert type(string_input) == str
	if "'" not in string_input:
		return string_input
	sql_input = ''
	for char in string_input:
		if char != "'":
			sql_input += char
	return sql_input


# --------- More preventive actions --------
# --------- More preventive actions --------


# --------- Public Information --------
# All users, whether logged in or not, can view this page
# a. Search for upcoming flights based on source city/airport name, destination city/airport name, date.
@app.route('/searchFlight', methods=['GET', 'POST'])
def searchFlight():
    departure_city = check_injection(request.form['departure_city'])
    departure_airport = check_injection(request.form['departure_airport'])
    arrival_city = check_injection(request.form['arrival_city'])
    arrival_airport = check_injection(request.form['arrival_airport'])
    departure_date = request.form['departure_date']
    arrival_date = request.form['arrival_date']

    cursor = conn.cursor()
    query = """
        SELECT * \
        FROM Flight, Airport \
        WHERE departure_airport = if (\'{}\' = '', departure_airport, \'{}\') AND \
            arrival_airport = if (\'{}\' = '', arrival_airport, \'{}\') AND \
            status = 'upcoming' AND \
            departure_city = if (\'{}\' = '', departure_city, \'{}\') AND \
            arrival_city = if (\'{}\' = '', arrival_city, \'{}\') AND \
            date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\') AND \
            date(arrival_time) = if (\'{}\' = '', date(arrival_time), \'{}\') \
		ORDER BY airline_name, flight_num
        """
    cursor.execute(query, (departure_airport, departure_airport, arrival_airport, arrival_airport, departure_city, departure_city, arrival_city, arrival_city, departure_date, departure_date, arrival_date, arrival_date))
    data = cursor.fetchall()
    cursor.close()

    if data: # has info
        return render_template('Home.html', upcoming_flights=data)
    else: # no info
        error = 'Sorry! We cannot find information about this flight.'
        return render_template('Home.html', error1=error)

# b. Will be able to see the flights status based on flight number, arrival/departure date.
@app.route('/searchFlightStatus', methods=['GET', 'POST'])
def searchFlightStatus():
    airline_name = check_injection(request.form['airline_name'])
    flight_num = check_injection(request.form['flight_num'])
    arrival_date = request.form['arrival_date']
    departure_date = request.form['departure_date']

    cursor = conn.cursor()
    query = """
        SELECT * \
		FROM Flight \
		WHERE flight_num = if (\'{}\' = '', flight_num, \'{}\') AND \
            date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\') AND \
            date(arrival_time) = if (\'{}\' = '', date(arrival_time), \'{}\') AND \
            airline_name = if (\'{}\' = '', airline_name, \'{}\') \
		ORDER BY airline_name, flight_num
        """
    cursor.execute(query, (flight_num, flight_num, arrival_date, arrival_date, departure_date, departure_date, airline_name, airline_name))
    data = cursor.fetchall() 
    cursor.close()
    
    if data: # has info
        return render_template('Home.html', statuses=data)
    else: # no info
        error = 'Sorry! We cannot find information about this flight.'
        return render_template('Home.html', error2=error)


# -------- Three Types of Registration -----------
@app.route('/register/customer')
def registerCustomer():
    return render_template('registerCustomer.html')

@app.route('/register/agent')
def registerAgent():
    return render_template('registerBookingAgent.html')

@app.route('/register/staff')
def registerStaff():
    return render_template('registerAirlineStaff.html')


# -------- Three Types of Registration Authentication -----------
# note that password needs to be hashed before saving to database
# 1. customer registration authentication
@app.route('/register/customer/auth', methods=['GET', 'POST'])
def registerCustomerAuth():
    email = check_injection(request.form['email'])
    name = check_injection(request.form['name'])
    password = request.form['password']
    building_number = check_injection(request.form['building_number'])
    street = check_injection(request.form['street'])
    city = check_injection(request.form['city'])
    state = check_injection(request.form['state'])
    phone_number = check_injection(request.form['phone_number'])
    passport_number = check_injection(request.form['passport_number'])
    passport_expiration = check_injection(request.form['passport_expiration'])
    passport_country = check_injection(request.form['passport_country'])
    date_of_birth = check_injection(request.form['date_of_birth'])
    
    if not len(password) >= 4:
        flash("Password length must be at least 4 characters. Please enter another password.")
        return redirect(request.url)

    cursor = conn.cursor()
    query = "SELECT * FROM Customer WHERE email = '{}'"
    cursor.execute(query.format(email))
    data = cursor.fetchone()
    error = None

    if data:
        error = "This user already exists. Please try logging in."
        return render_template('registerCustomer.html', error=error)
    
    else:
        try:
            ins = "INSERT INTO Customer VALUES(\'{}\', \'{}\', md5(\'{}\'), \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
            cursor.execute(ins.format(email, name, hashlib.md5(password.encode()).hexdigest(), 
                                        building_number, street, city, state, phone_number, 
                                        passport_number, passport_expiration, passport_country, date_of_birth))
            conn.commit()
            cursor.close()
        except:
            return render_template('registerCustomer.html', error='Failed to register user.')
        return redirect('/home/customer')

# 2. booking agent registration authentication
@app.route('/register/agent/auth', methods=['GET', 'POST'])
def registerAgentAuth():
    email = check_injection(request.form['email'])
    password = request.form['password']
    booking_agent_id = check_injection(request.form['booking_agent_id'])

    cursor = conn.cursor()
    query = "SELECT * FROM BookingAgent WHERE email = '{}'"
    cursor.execute(query.format(email))
    data = cursor.fetchone()
    error = None
    
    if data:
        error = "This user already exists. Please try logging in."
        return render_template('register.html', error=error)
    
    else:
        try:
            ins = "INSERT INTO BookingAgent VALUES(\'{}\', md5(\'{}\'), \'{}\')"
            cursor.execute(ins.format(email, hashlib.md5(password.encode()).hexdigest(), booking_agent_id))
            conn.commit()
            cursor.close()
        except:
            return render_template('register.html', error='Failed to register user.')
        return redirect('/bookingAgentHome')

# 3. airline staff registration authentication
@app.route('/register/staff/auth', methods=['GET', 'POST'])
def registerStaffAuth():
    username = check_injection(request.form['username'])
    password = request.form['password']
    first_name = check_injection(request.form['first_name'])
    last_name = check_injection(request.form['last_name'])
    date_of_birth = check_injection(request.form['date_of_birth'])
    airline_name = check_injection(request.form['airline_name'])

    cursor = conn.cursor()
    query = "SELECT * FROM AirlineStaff WHERE username = '{}'"
    cursor.execute(query.format(username))
    data = cursor.fetchone()
    error = None

    if data:
        error = "This user already exists. Please try logging in."
        return render_template('register.html', error=error)
    
    else:
        try:
            ins = "INSERT INTO airline_staff VALUES(\'{}\', md5(\'{}\'), \'{}\', \'{}\', \'{}\', \'{}\')"
            cursor.execute(ins.format(username, hashlib.md5(password.encode()).hexdigest(), first_name, last_name, date_of_birth, airline_name))
            conn.commit()
            cursor.close()
        except:
            return render_template('register.html', error=True)
        return redirect('/airlineStaffHome')


# -------- Three Types of Users Login -----------
@app.route('/login/customer')
def loginCustomer():
    return render_template('loginCustomer.html')

@app.route('/login/agent')
def loginAgent():
    return render_template('loginAgent.html')

@app.route('/login/staff')
def loginStaff():
    return render_template('loginStaff.html')


# -------- Three Types of Users Login Authentication -----------
# 1. customer login authentication
@app.route('/login/customer/auth', methods=['GET', 'POST'])
def loginCustomerAuth():
    email = check_injection(request.form['email'])
    password = request.form['password']

    cursor = conn.cursor()
    query = "SELECT * FROM customer WHERE email = '{}' and password = '{}'"
    cursor.execute(query.format(email, hashlib.md5(password.encode()).hexdigest()))
    data = cursor.fetchone()
    cursor.close()
    error = None

    if data:
        session['customer'] = email
        return redirect("/customerHome")

    else:
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

# 2. booking agent login authentication
@app.route('/login/agent/auth', methods=['GET', 'POST'])
def loginAgentAuth():
    # grabs information from the forms
    email = check_injection(request.form['email'])
    password = request.form['password']

    cursor = conn.cursor()
    query = "SELECT * FROM booking_agent WHERE email = '{}' and password = '{}'"
    cursor.execute(query.format(email, hashlib.md5(password.encode()).hexdigest()))
    data = cursor.fetchone()
    cursor.close()
    error = None

    if data:
        session['bookingAgent'] = email
        return redirect("/bookingAgentHome")
    else:
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

# 3. staff login authentication
@app.route('/login/staff/auth', methods=['GET', 'POST'])
def loginStaffAuth():
    username = check_injection(request.form['username'])
    password = request.form['password']

    cursor = conn.cursor()
    query = "SELECT * FROM airline_staff WHERE username = '{}' and password = '{}'"
    cursor.execute(query.format(username, hashlib.md5(password.encode()).hexdigest()))
    data = cursor.fetchone()
    cursor.close()
    error = None

    if data:
        session['airlineStaff'] = [username, data[-1]] # associated airline
        return redirect('/staffHome')
    else:
        error = 'Invalid login or username'
        return render_template('login.html', error=error)


# -------- General Use Cases for Three Users -----------
# 1. View My Flights

# 2. Search for Flights

# 3. Logout
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


# -------- Customer Exlusive Use Cases -----------
# 1. Customer Homepage
@app.route('/home/customer')
def homeCustomer():
	if session.get('email'):
		email = check_injection(session['email'])

		cursor = conn.cursor()
		query = "SELECT ticket_id, airline_name, airplane_id, flight_num, \
			D.airport_city, \
			departure_airport, A.airport_city, arrival_airport, departure_time, arrival_time, status \
				FROM flight NATURAL JOIN purchases NATURAL JOIN ticket, airport as D, airport as A\
					WHERE customer_email = \'{}\' and status = 'upcoming' and \
					D.airport_name = departure_airport and A.airport_name = arrival_airport"
		cursor.execute(query.format(email))
		data1 = cursor.fetchall() 
		cursor.close()
		return render_template('customerHome.html', email=email, emailName=email.split('@')[0], view_my_flights=data1)
	else:
		session.clear()
		return render_template('404.html')

# 2. Customer Purchase Tickets
@app.route('/purchase/customer', methods=['GET', 'POST'])
def purchaseCustomer():
	if session.get('email'):
		email = session['email']
		db_email = check_apostrophe(email)
		airline_name = check_apostrophe(request.form['airline_name'])
		flight_num = request.form['flight_num']

		cursor = conn.cursor()
		# query = "SELECT ticket_id \
		# 		FROM flight NATURAL JOIN ticket \
		# 		WHERE flight_num = \'{}\' AND \
		# 			ticket_id NOT IN (SELECT ticket_id \
		# 								FROM flight NATURAL JOIN ticket NATURAL JOIN purchases)\
		# 			AND flight_num = \'{}\'"
		# there is no extra failsafe anymore 
		query = "SELECT * \
				FROM flight \
				WHERE airline_name = \'{}\' AND flight_num = \'{}\' AND num_tickets_left > 0"
		cursor.execute(query.format(airline_name, flight_num))
		# cursor.execute(query.format(flight_num, flight_num))
		data = cursor.fetchall()
		cursor.close()

		if(data):
			cursor = conn.cursor()
			# calc the new ticket id = biggest id + 1
			cursor = conn.cursor()
			query_id = "SELECT ticket_id \
						FROM ticket \
						ORDER BY ticket_id DESC \
						LIMIT 1"
			cursor.execute(query_id)
			ticket_id_data = cursor.fetchone() # (74373,)
			new_ticket_id = int(ticket_id_data[0]) + 1
			# first insert into ticket
			ins1 = "INSERT INTO ticket VALUES (\'{}\', \'{}\', \'{}\')"
			cursor.execute(ins1.format(new_ticket_id, airline_name, flight_num))
			# then insert into purchases
			ins = "INSERT INTO purchases VALUES (\'{}\', \'{}\', NULL, CURDATE())"
			cursor.execute(ins.format(new_ticket_id, db_email))
			conn.commit()
			cursor.close()
			message1 = 'Ticket bought successfully!'
			return render_template('cusSearchPurchase.html', email = email, message1 = message1)
		else:
			error = 'No ticket'
			return render_template('cusSearchPurchase.html', error2=error, email = email, emailName=email.split('@')[0])
	else:
		session.clear()
		return render_template('404.html')

# 3. Track My Spending


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
