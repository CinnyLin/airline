### REQUIREMENTS ### (delete when complete)
# 5. home page should deal with error message and link to other interfaces
# 6. general use cases: ViewMyFlights, SearchFlights, Logout
# 7. Customer: PurchaseTickets, TrackMySpending
# 8. BookingAgent: PurchaseTickets, ViewMyCommission, ViewTopCustomers
# 9. AirlineStaff: CreateNewFlights, ChangeFlightStatus, AddAirplane, AddAirport, 
#           ViewBookingAgents, ViewReports, RevenueComparison, ViewTopDestinations
# 10. enforce constraints: e.g. customer can't create new flights

### ADDITIONAL FEATURES ###
# 1. choose to book one-way or round-trip
# 2. chatbot connects to booking agent to automatically book for you

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
# for Cinny: don't need password, database name is "airline"
# for Zoe: need password, database name is "air"
conn = mysql.connector.connect(host='localhost',
                               user='root',
                               #password='password',  # comment out this line if not needed
                               database='airline',
                               port=3306)


# Define route for login
@app.route('/')
def index():
    return render_template('login.html')


# --------- Prevent SQL injection --------
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


# --------- Public Information: Search Flights  --------
# All users, whether logged in or not, can view this page
# PROBLEM: Customers and booking agents have "search flights" function can they use this function?

# 1. Search flights based on source city/airport name, destination city/airport name, date.
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

# 2. Search flights status based on flight number, arrival/departure date.
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
# PROBLEM: with the current template, i don't know which date is birthday and which date is passport expiration
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
# Note that password needs to be hashed before saving to database

# 1. Customer Registration Authentication
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

# 2. Booking Agent Registration Authentication
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
        return redirect('/homeBookingAgent')

# 3. Airline Staff Registration Authentication
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
        return redirect('/homeAirlineStaff')


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

# 1. Customer Login Authentication
# PROBLEM: currently when i register, it prompts me to login because my name was already in the database,
# but when i try to log in it brings me back to register page instead of prompting me to CustomerHome
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
        return redirect("/homeCustomer")

    else:
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

# 2. Booking Agent Login Authentication
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
        return redirect("/homeBookingAgent")
    else:
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

# 3. Staff Login Authentication
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


# -------- Three Types of Users Logout -----------
@app.route('/logout')
def logout():
    session.clear() #session.pop('username')
    return redirect('/')


# -------- Customer Exlusive Use Cases -----------
# 1. Customer Homepage
@app.route('/home/customer')
def homeCustomer():
	if session.get('email'):
		email = check_injection(session['email'])

		cursor = conn.cursor()
		query = """
        SELECT ticket_id, airline_name, airplane_id, flight_num, A1.airport_city, 
        departure_airport, A2.airport_city, arrival_airport, departure_time, arrival_time, status \
		FROM flight NATURAL JOIN purchase NATURAL JOIN ticket, airport AS A2, airport AS A1\
		WHERE customer_email = \'{}\' AND status = 'upcoming' AND \
		A2.airport_name = departure_airport AND A1.airport_name = arrival_airport"""
		cursor.execute(query.format(email))
		data = cursor.fetchall() 
		cursor.close()
		return render_template('homeCustomer.html', email=email, emailName=email.split('@')[0], view_my_flights=data)
	else:
		session.clear()
		return render_template('404.html')


# 2. Customer View Flights
# Provide various ways for the user to see flights information they purchased. 
# The default should show upcoming flights. Optionally, you may allow user to specify a
# range of dates, specify destination and/or source airport name or city name etc.


# 3. Customer Purchase Tickets
# Customer chooses a flight and purchase ticket for this flight. 
# PROBLEM: Implement this along with a use case to search for flights.
@app.route('/home/customer/purchase', methods=['GET', 'POST'])
def purchaseTicket():
	if session.get('email'):
		email = check_injection(email)
		airline_name = check_injection(request.form['airline_name'])
		flight_num = request.form['flight_num']

		cursor = conn.cursor()
		query = """
        SELECT ticket_id \
		FROM flight NATURAL JOIN ticket \
		WHERE flight_num = \'{}\' AND ticket_id NOT IN \
            (SELECT ticket_id \
		    FROM flight NATURAL JOIN ticket NATURAL JOIN purchase)\
		AND flight_num = \'{}\'"""
		cursor.execute(query.format(airline_name, flight_num))
		data = cursor.fetchall()
		cursor.close()

		if(data):
			cursor = conn.cursor()
			query_id = "SELECT ticket_id \
						FROM ticket \
						ORDER BY ticket_id DESC \
						LIMIT 1"
			cursor.execute(query_id)
			ticket_id_data = cursor.fetchone() # (74373,)
			new_ticket_id = int(ticket_id_data[0]) + 1
			insert1 = "INSERT INTO ticket VALUES (\'{}\', \'{}\', \'{}\')"
			cursor.execute(insert1.format(new_ticket_id, airline_name, flight_num))
			insert2 = "INSERT INTO purchases VALUES (\'{}\', \'{}\', NULL, CURDATE())"
			cursor.execute(insert2.format(new_ticket_id, email))
			conn.commit()
			cursor.close()
			message1 = 'Ticket bought successfully!'
			return render_template('customerPurchase.html', email=email, message1=message1)
		else:
			error = 'No ticket found.'
			return render_template('customerPurchase.html', error2=error, email=email, emailName=email.split('@')[0])
	else:
		session.clear()
		return render_template('404.html')

# 4. Track My Spending




# ------- Booking Agent Exclusive Functions --------

# 1. Booking Agent Purchased Ticket


# 2. Booking Agent View Commissions

# 3. Booking Agent View Top Customers




# ------ Airline Staff Exclusieve Functions -------

# 1. Airline Staff Create New Flights


# 2. Airline Staff Change Flight Status



# 3. Airline Staff Add New Airplane


# 4. Airline Staff Add Airport


# 5. Airline Staff View Booking Agents 
# Top 5 booking agents based on number of tickets sales for the past month and past year. 
# Top 5 booking agents based on the amount of commission received for the last year.


# 6. Airline Staff View Frequent Customers
# Airline Staff will also be able to see the most frequent customer within the last year. 
# In addition, Airline Staff will be able to see a list of all flights a particular 
# Customer has taken only on that particular airline.


# 7. Airline Staff View Reports 
# Total amounts of ticket sold based on range of dates/last year/last month etc. 
# Month-wise tickets sold in a bar chart.


# 8. Airline Staff Revenue Comparison
# Draw a pie chart for showing total amount of revenue earned from direct sales 
# (when customer bought tickets without using a booking agent) and total amount 
# of revenue earned from indirect sales (when customer bought tickets using 
# booking agents) in the last month and last year


# 9. Airline Staff View Top Destinations 
# Find the top 3 most popular destinations for last 3 months and last year.




app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
