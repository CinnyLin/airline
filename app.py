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
                               password='',
                               database='airline')
                               #port=3306)


# Define a route to hello function
@app.route('/')
def hello():
    if 'Customer' in session:
        return redirect('/CustomerHome')
    elif 'BookingAgent' in session:
        return redirect('/BookingAgentHome')
    elif 'AirlineStaff' in session:
        return redirect('/AirlineStaffHome')
    else:
        return render_template('index.html')

# Define route for home
@app.route('/index')
def index():
    return render_template('index.html')

# Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

# Define route for register
@app.route('/register')
def register():
    return render_template('register.html')


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


# --------- Public Information --------
# 1. View Public Info: All users, whether logged in or not, can
@app.route('/')
def publicHome():
	return render_template('Home.html')

# a. Search for upcoming flights based on source city/airport name, destination city/airport name, date.
@app.route('/SearchFlight', methods=['GET', 'POST'])
def SearchFlight():
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
@app.route('/SearchFlightStatus', methods=['GET', 'POST'])
def SearchFlightStatus():
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


# -------- Three Types of Registrations -----------
# note that password needs to be hashed before saving to database

# 1. customer regitsrtaion authentication
@app.route('/Register', methods=['GET', 'POST'])
def Register():
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
        return render_template('register.html', error=error)
    
    else:
        try:
            ins = "INSERT INTO Customer VALUES(\'{}\', \'{}\', md5(\'{}\'), \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
            cursor.execute(ins.format(email, name, hashlib.md5(password.encode()).hexdigest(), 
                                        building_number, street, city, state, phone_number, 
                                        passport_number, passport_expiration, passport_country, date_of_birth))
            conn.commit()
            cursor.close()
        except:
            return render_template('register.html', error='Failed to register user.')
        return redirect('/login')


# 2. booking agent registration authentication
@app.route('/AgentRegister', methods=['GET', 'POST'])
def AgentRegister():
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
        return redirect('/login')

# 3. airline staff registration authentication
@app.route('/StaffRegister', methods=['GET', 'POST'])
def StaffRegister():
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
        return redirect('/login')


# -------- Three Types of Users Login -----------
# 1. customer login authentication
@app.route('/Login', methods=['GET', 'POST'])
def Login():
    email = check_injection(request.form['email'])
    password = request.form['password']

    cursor = conn.cursor()
    query = "SELECT * FROM customer WHERE email = '{}' and password = '{}'"
    cursor.execute(query.format(email, hashlib.md5(password.encode()).hexdigest()))
    data = cursor.fetchone()
    cursor.close()
    error = None

    if data:
        session['Customer'] = email
        return redirect("/CustomerHome")

    else:
        error = 'Invalid login or username'
        return render_template('login.html', error=error)


# 2. booking agent login authentication
@app.route('/AgentLogin', methods=['GET', 'POST'])
def AgentLogin():
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
        session['BookingAgent'] = email
        return redirect("/BookingAgentHome")
    else:
        error = 'Invalid login or username'
        return render_template('login.html', error=error)


# 3. staff login authentication
@app.route('/StaffLogin', methods=['GET', 'POST'])
def StaffLogin():
    username = check_injection(request.form['username'])
    password = request.form['password']

    cursor = conn.cursor()
    query = "SELECT * FROM airline_staff WHERE username = '{}' and password = '{}'"
    cursor.execute(query.format(username, hashlib.md5(password.encode()).hexdigest()))
    data = cursor.fetchone()
    cursor.close()
    error = None

    if data:
        session['AirlineStaff'] = [username, data[-1]] # associated airline
        return redirect('/StaffHome')
    else:
        error = 'Invalid login or username'
        return render_template('login.html', error=error)




@app.route('/home')
def home():

    username = session['username']
    cursor = conn.cursor()
    query = "SELECT ts, blog_post FROM blog WHERE username = \'{}\' ORDER BY ts DESC"
    cursor.execute(query.format(username))
    data1 = cursor.fetchall()
    cursor.close()
    return render_template('home.html', username=username, posts=data1)


@app.route('/post', methods=['GET', 'POST'])
def post():
    username = session['username']
    cursor = conn.cursor()
    blog = request.form['blog']
    query = "INSERT INTO blog (blog_post, username) VALUES(\'{}\', \'{}\')"
    cursor.execute(query.format(blog, username))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
