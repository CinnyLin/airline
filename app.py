### ADDITIONAL FEATURES TO WORK ON ###
# 11. where you have been: map for customers tickets bought and staff destinations

### ADDITIONAL FEATURES WE DID ###
# 1. delete account and reset password
# 2. check session every time and identity resolution by separate routing for users
# 3. SQL injection check
# 4. password length check
# 5. check seat to num_tickets matches when airline staff add data


# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify
import mysql.connector
import hashlib
from datetime import datetime, date
import json


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


# Define route for home page
@app.route('/')
def index():
    return render_template('index.html') 

# --------- Prevent SQL injection --------
def check_injection(string_input):
    assert type(string_input) == str
    if "'" not in string_input:
        return string_input
    sql_input = ""
    for char in string_input:
        if char != "'":
            sql_input += char
    return sql_input

# --------- Public Information: Search Flights  --------
# All users, whether logged in or not, can view this page

# 1. Search flights based on source city/airport name, destination city/airport name, date.
@app.route('/search/flight', methods=['GET', 'POST'])
def searchFlight():
    departure_city = check_injection(request.form['departure_city'])
    departure_airport = check_injection(request.form['departure_airport'])
    departure_time = request.form['departure_time']
    arrival_city = check_injection(request.form['arrival_city'])
    arrival_airport = check_injection(request.form['arrival_airport'])
    arrival_time = request.form['arrival_time']
    airline_name = request.form['airline_name']
    price = request.form['price']

    cursor = conn.cursor()
    query = """
        SELECT airline_name, flight_num, 
                departure_airport, Depart.airport_city, departure_time,
                arrival_airport, Arrive.airport_city, arrival_time, 
                status, price, num_tickets_left \
        FROM flight, airport AS Depart, airport AS Arrive \
        WHERE departure_airport = if (\'{}\' = '', departure_airport, \'{}\') AND \
            Depart.airport_city = if (\'{}\' = '', Depart.airport_city, \'{}\') AND \
            Depart.airport_name = departure_airport AND \
            date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\') AND \
            arrival_airport = if (\'{}\' = '', arrival_airport, \'{}\') AND \
            Arrive.airport_city = if (\'{}\' = '', Arrive.airport_city, \'{}\') AND \
            Arrive.airport_name = arrival_airport AND \
            date(arrival_time) = if (\'{}\' = '', date(arrival_time), \'{}\') AND \
            airline_name = if (\'{}\' = '', airline_name, \'{}\') AND \
            price <= if (\'{}\' = '', price, \'{}\') AND \
            status = 'upcoming'
		ORDER BY airline_name, flight_num
        """
    cursor.execute(query.format(
        departure_airport, departure_airport, departure_city, departure_city, departure_time, departure_time,
        arrival_airport, arrival_airport, arrival_city, arrival_city, arrival_time, arrival_time,
        airline_name, airline_name, price, price))
    data = cursor.fetchall()
    cursor.close()

    if data:
        return render_template('publicSearchFlights.html', upcoming_flights=data)
    else:
        error = 'Sorry! This flight is not in our database.'
        return render_template('index.html', error1=error)

# 2. Search flights status based on flight number, arrival/departure date.
@app.route('/search/flightStatus', methods=['GET', 'POST'])
def searchFlightStatus():
    airline_name = check_injection(request.form['airline_name'])
    flight_num = check_injection(request.form['flight_num'])
    ticket_id = check_injection(request.form['ticket_id'])

    cursor = conn.cursor()
    
    query = """
        SELECT ticket_id, airline_name, flight_num, status,
            departure_airport, Depart.airport_city, departure_time,
            arrival_airport, Arrive.airport_city, arrival_time \
		FROM flight NATURAL JOIN ticket, airport AS Depart, airport AS Arrive \
		WHERE Depart.airport_name = departure_airport AND \
            Arrive.airport_name = arrival_airport AND \
            flight_num = if (\'{}\' = '', flight_num, \'{}\') AND \
            airline_name = if (\'{}\' = '', airline_name, \'{}\') AND \
            ticket_id = if (\'{}\' = '', ticket_id, \'{}\') \
		ORDER BY airline_name, flight_num
        """
    cursor.execute(query.format(
        flight_num, flight_num, airline_name, airline_name, ticket_id, ticket_id))
    data = cursor.fetchall() 
    cursor.close()
    
    if data:
        return render_template('publicSearchFlightStatus.html', flight_statuses=data)
    else:
        error = 'Sorry! We cannot find information about this flight.'
        return render_template('index.html', error2=error)


### ------- User Type Account Settings ----------

# -------- Three Types of Registration -----------
# Password is hashed before saving to database

# @app.route('/register')
# def register():
#     return render_template('register.html')

@app.route('/register/customer')
def registerCustomer():
    return render_template('registerCustomer.html')

@app.route('/register/agent')
def registerAgent():
    return render_template('registerAgent.html')

@app.route('/register/staff')
def registerStaff():
    return render_template('registerStaff.html')


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
    query = "SELECT * FROM customer WHERE email = \'{}\'"
    cursor.execute(query.format(email))
    data = cursor.fetchone()
    error = None

    if data:
        error = "This user already exists. Please try logging in."
        return render_template('registerCustomer.html', error=error)
    
    else:
        try:
            insert = "INSERT INTO customer VALUES(\'{}\', \'{}\', md5(\'{}\'), \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
            cursor.execute(insert.format(email, name, hashlib.md5(password.encode()).hexdigest(), 
                                        building_number, street, city, state, phone_number, 
                                        passport_number, passport_expiration, passport_country, date_of_birth))
            conn.commit()
            cursor.close()
        except:
            return render_template('registerCustomer.html', error='Failed to register customer.')
        session['email'] = email
        return redirect('/customer/home')

# 2. Booking Agent Registration Authentication
@app.route('/register/agent/auth', methods=['GET', 'POST'])
def registerAgentAuth():
    email = check_injection(request.form['email'])
    password = request.form['password']
    booking_agent_id = check_injection(request.form['booking_agent_id'])

    if not len(password) >= 4:
        flash("Password length must be at least 4 characters. Please enter another password.")
        return redirect(request.url)

    cursor = conn.cursor()
    query = "SELECT * FROM bookingAgent WHERE email = \'{}\'"
    cursor.execute(query.format(email))
    data = cursor.fetchone()
    error = None
    
    if data:
        error = "This user already exists. Please try logging in."
        return render_template('registerAgent.html', error=error)
    
    else:
        try:
            insert = "INSERT INTO bookingAgent VALUES(\'{}\', md5(\'{}\'), \'{}\')"
            cursor.execute(insert.format(email, hashlib.md5(password.encode()).hexdigest(), booking_agent_id))
            conn.commit()
            cursor.close()
        except:
            return render_template('registerAgent.html', error='Failed to register agent.')
        session['email'] = email
        return redirect('/agent/home')

# 3. Airline Staff Registration Authentication
@app.route('/register/staff/auth', methods=['GET', 'POST'])
def registerStaffAuth():
    username = check_injection(request.form['username'])
    password = request.form['password']
    first_name = check_injection(request.form['first_name'])
    last_name = check_injection(request.form['last_name'])
    date_of_birth = check_injection(request.form['date_of_birth'])
    airline_name = check_injection(request.form['airline_name'])

    if not len(password) >= 4:
        flash("Password length must be at least 4 characters. Please enter another password.")
        return redirect(request.url)

    cursor = conn.cursor()
    query = "SELECT * FROM airlineStaff WHERE username = \'{}\'"
    cursor.execute(query.format(username))
    data = cursor.fetchone()
    error = None

    if data:
        error = "This user already exists. Please try logging in."
        return render_template('registerStaff.html', error=error)
    
    else:
        try:
            insert = "INSERT INTO airlineStaff VALUES(\'{}\', md5(\'{}\'), \'{}\', \'{}\', \'{}\', \'{}\')"
            cursor.execute(insert.format(username, hashlib.md5(password.encode()).hexdigest(), 
                            first_name, last_name, date_of_birth, airline_name))
            conn.commit()
            cursor.close()
        except:
            return render_template('registerStaff.html', error='Airline does not exist.')
            # airlineStaff has airline_name being foreign key when register so would fail if airline does not exist
        session['username'] = username
        return redirect('/staff/home')


# -------- Three Types of Users Login -----------
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/customer')
def loginCustomer():
    return render_template('loginCustomer.html')

@app.route('/login/agent')
def loginAgent():
    return render_template('loginAgent.html')

@app.route('/login/staff')
def loginStaff():
    return render_template('loginStaff.html')

# 1. Customer Login Authentication
@app.route('/login/customer/auth', methods=['GET', 'POST'])
def loginCustomerAuth():
    if 'email' in request.form and 'password' in request.form:
        email =check_injection(request.form['email'])
        password = request.form['password']
        
        cursor = conn.cursor()
        query = "SELECT * FROM customer WHERE email = \'{}\' and password = md5(\'{}\')"
        cursor.execute(query.format(email, hashlib.md5(password.encode()).hexdigest()))
        data = cursor.fetchone()
        cursor.close()
        
        if data:
            session['email'] = email
            return redirect("/customer/home")
        else:
            error = 'Invalid login or email.'
            return render_template('loginCustomer.html', error=error)
    
    else:
        session.clear()
        return render_template('404.html')


# 2. Booking Agent Login Authentication
@app.route('/login/agent/auth', methods=['GET', 'POST'])
def loginAgentAuth():
    email = check_injection(request.form['email'])
    password = request.form['password']

    cursor = conn.cursor()
    query = "SELECT * FROM bookingAgent WHERE email = \'{}\' and password = md5(\'{}\')"
    cursor.execute(query.format(email, hashlib.md5(password.encode()).hexdigest()))
    data = cursor.fetchone()
    cursor.close()
    error = None

    if data:
        session['email'] = email
        return redirect("/agent/home")
    else:
        error = 'Invalid login or username.'
        return render_template('loginAgent.html', error=error)

# 3. Staff Login Authentication
@app.route('/login/staff/auth', methods=['GET', 'POST'])
def loginStaffAuth():
    username = check_injection(request.form['username'])
    password = request.form['password']

    cursor = conn.cursor()
    query = "SELECT * FROM airlineStaff WHERE username = \'{}\' and password = md5(\'{}\')"
    cursor.execute(query.format(username, hashlib.md5(password.encode()).hexdigest()))
    data = cursor.fetchone()
    cursor.close()
    error = None

    if data:
        session['username'] = username # should consider airline?
        return redirect('/staff/home')
    else:
        error = 'Invalid login or username.'
        return render_template('loginStaff.html', error=error)


# -------- Logout Function -----------
@app.route('/logout')
def logout():
    session.clear() #session.pop('username')
    return redirect('/')


# -------- Three Types of Users Delete Account -----------

# @app.route('/deleteAccount')
# def deleteAccount():
#     session.clear()
#     return redirect('/')

@app.route('/deleteAccount/customer')
def deleteAccountCustomer():
    return render_template('deleteCustomer.html')

@app.route('/deleteAccount/agent')
def deleteAccountAgent():
    return render_template('deleteAgent.html')

@app.route('/deleteAccount/staff')
def deleteAccountStaff():
    return render_template('deleteStaff.html')

# 1. Customer Delete Account Authentication
@app.route('/deleteAccount/customer/auth', methods=['GET', 'POST'])
def deleteAccountCustomerAuth():
    if 'email' in request.form and 'password' in request.form:
        email =check_injection(request.form['email'])
        password = request.form['password']
        
        cursor = conn.cursor()
        query = "DELETE FROM customer WHERE email = \'{}\' and password = md5(\'{}\')"
        cursor.execute(query.format(email, hashlib.md5(password.encode()).hexdigest()))
        conn.commit()
        cursor.close()
        
        message = 'Your account is successfully deleted. We are sorry to see you go!'
        return render_template('deleteCustomer.html', message=message)
        
    else:
        session.clear()
        return render_template('404.html')

# 2. Booking Agent Delete Account Authentication
@app.route('/deleteAccount/agent/auth', methods=['GET', 'POST'])
def deleteAccountAgentAuth():
    if 'email' in request.form and 'password' in request.form:
        email =check_injection(request.form['email'])
        password = request.form['password']
        
        cursor = conn.cursor()
        query = "DELETE FROM bookingAgent WHERE email = \'{}\' and password = md5(\'{}\')"
        cursor.execute(query.format(email, hashlib.md5(password.encode()).hexdigest()))
        conn.commit()
        cursor.close()
        
        message = 'Your account is successfully deleted.'
        return render_template('deleteAgent.html', message=message)

    else:
        session.clear()
        return render_template('404.html')

# 3. Airline Staff Delete Account Authentication
@app.route('/deleteAccount/staff/auth', methods=['GET', 'POST'])
def deleteAccountStaffAuth():
    if 'username' in request.form and 'password' in request.form:
        username =check_injection(request.form['username'])
        password = request.form['password']
        
        cursor = conn.cursor()
        query = "DELETE FROM airlineStaff WHERE username = \'{}\' and password = md5(\'{}\')"
        cursor.execute(query.format(username, hashlib.md5(password.encode()).hexdigest()))
        conn.commit()
        cursor.close()
        
        message = 'Your account is successfully deleted.'
        return render_template('deleteStaff.html', message=message)

    else:
        session.clear()
        return render_template('404.html')

# -------- Three Types of Users Reset Password -----------

@app.route('/resetPassword/customer')
def resetPasswordCustomer():
    return render_template('resetCustomer.html')

@app.route('/resetPassword/agent')
def resetPasswordAgent():
    return render_template('resetAgent.html')

@app.route('/resetPassword/staff')
def resetPasswordStaff():
    return render_template('resetStaff.html')

# 1. Customer Reset Password Authentication
@app.route('/resetPassword/customer/auth', methods=['GET', 'POST'])
def resetPasswordCustomerAuth():
    if ('email' in request.form) and \
        ('old_password' in request.form) and \
        ('new_password' in request.form):
        email =check_injection(request.form['email'])
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        cursor = conn.cursor()
        query = """
            UPDATE customer
            SET password = md5(\'{}\')
            WHERE email = \'{}\' AND password = md5(\'{}\')"""
        cursor.execute(query.format(
            hashlib.md5(new_password.encode()).hexdigest(),
            email, 
            hashlib.md5(old_password.encode()).hexdigest()))
        conn.commit()
        cursor.close()

        message = 'Your password is successfully changed. Please log in again.'
        return render_template('loginCustomer.html', message=message)

    else:
        session.clear()
        return render_template('404.html')

# 2. Agent Reset Password Authentication
@app.route('/resetPassword/agent/auth', methods=['GET', 'POST'])
def resetPasswordAgentAuth():
    if ('email' in request.form) and \
        ('old_password' in request.form) and \
        ('new_password' in request.form):
        email =check_injection(request.form['email'])
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        cursor = conn.cursor()
        query = """
            UPDATE bookingAgent
            SET password = md5(\'{}\')
            WHERE email = \'{}\' AND password = md5(\'{}\')"""
        cursor.execute(query.format(
            hashlib.md5(new_password.encode()).hexdigest(),
            email, 
            hashlib.md5(old_password.encode()).hexdigest()))
        conn.commit()
        cursor.close()
        
        message = 'Your password is successfully changed. Please log in again.'
        return render_template('loginAgent.html', message=message)


    else:
        session.clear()
        return render_template('404.html')

# 3. Staff Reset Password Authentication
@app.route('/resetPassword/staff/auth', methods=['GET', 'POST'])
def resetPasswordStaffAuth():
    if ('email' in request.form) and \
        ('old_password' in request.form) and \
        ('new_password' in request.form):
        username =check_injection(request.form['username'])
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        
        cursor = conn.cursor()
        query = """
            UPDATE airlineStaff
            SET password = md5(\'{}\')
            WHERE email = \'{}\' AND password = md5(\'{}\')"""
        cursor.execute(query.format(
            hashlib.md5(new_password.encode()).hexdigest(),
            username, 
            hashlib.md5(old_password.encode()).hexdigest()))
        conn.commit()
        cursor.close()
        
        message = 'Your password is successfully changed. Please log in again.'
        return render_template('loginStaff.html', message=message)

    else:
        session.clear()
        return render_template('404.html')


### ------- User Type Exclusive Use Cases -------

# -------- Customer Exlusive Use Cases -----------
# 1. Customer Homepage
@app.route('/customer/home')
def homeCustomer():
    if session.get('email'):
        email = session['email']
        cursor = conn.cursor()
        query = "SELECT name FROM customer WHERE email = \'{}\'"
        cursor.execute(query.format(email))
        username = cursor.fetchone()
        username = str(username)[2:-3]
        cursor.close()
        return render_template('homeCustomer.html', email=email, username=username)
    
    else:
        session.clear()
        return render_template('404.html')

# 2. Customer View Flights
# Provide various ways for the user to see flights information they purchased. 
# The default should show upcoming flights. 
# Optionally, you may allow user to specify a range of dates, 
# specify destination and/or source airport name or city name etc.
@app.route('/customer/viewTickets')
def customerViewTickets():
    if session.get('email'):
        email = check_injection(session['email'])
        
        cursor = conn.cursor()
        query = """
            SELECT ticket_id, airline_name, flight_num, 
            Depart.airport_city, departure_airport, Arrive.airport_city, arrival_airport, 
            departure_time, arrival_time, status \
            FROM flight NATURAL JOIN purchase NATURAL JOIN ticket, \
                airport AS Arrive, airport AS Depart\
            WHERE customer_email = \'{}\' AND status = 'upcoming' AND \
            Depart.airport_name = departure_airport AND Arrive.airport_name = arrival_airport"""
        cursor.execute(query.format(email))
        flight_data = cursor.fetchall() 
        cursor.close()
        
        cursor = conn.cursor()
        query2 = "SELECT name FROM customer WHERE email = \'{}\'"
        cursor.execute(query2.format(email))
        username = cursor.fetchone()
        username = str(username)[2:-3]
        cursor.close()
        
        return render_template('customerViewTicket.html', email=email, username=username, flight_data=flight_data)
    
    else:
        session.clear()
        return render_template('404.html')

# 3. Customer Search Flights and Purchase Tickets
@app.route('/customer/search&purchase', methods=['GET', 'POST'])
def customerSearchPurchase():
    if session.get('email'):
        email = check_injection(session['email'])
        cursor = conn.cursor()
        query = "SELECT name FROM customer WHERE email = \'{}\'"
        cursor.execute(query.format(email))
        username = cursor.fetchone()
        username = str(username)[2:-3]
        cursor.close()
    return render_template('customerSearchFlight.html', username=username)

# (1) Customer Search Flights
@app.route('/customer/searchFlights', methods=['GET', 'POST'])
def customerSearchFlights():
    if session.get('email'):
        email = check_injection(session['email'])
        departure_city = check_injection(request.form['departure_city'])
        departure_airport = check_injection(request.form['departure_airport'])
        departure_time = request.form['departure_time']
        arrival_city = check_injection(request.form['arrival_city'])
        arrival_airport = check_injection(request.form['arrival_airport'])
        arrival_time = request.form['arrival_time']
        airline_name = request.form['airline_name']
        price = request.form['price']

        cursor = conn.cursor()
        query = "SELECT name FROM customer WHERE email = \'{}\'"
        cursor.execute(query.format(email))
        username = cursor.fetchone()
        username = str(username)[2:-3]
        cursor.close()
        
        cursor = conn.cursor()
        query = """
            SELECT airplane_id, flight_num, 
                Depart.airport_city, departure_airport, 
                Arrive.airport_city, arrival_airport, 
                departure_time, arrival_time, 
                status, price, airline_name, num_tickets_left \
            FROM airport AS Depart, flight, airport AS Arrive \
            WHERE Depart.airport_city = if (\'{}\' = '',Depart.airport_city, \'{}\') AND \
                Depart.airport_name = departure_airport AND \
                departure_airport = if (\'{}\' = '', departure_airport, \'{}\') AND \
                Arrive.airport_city = if (\'{}\' = '', Arrive.airport_city, \'{}\')AND \
                Arrive.airport_name = arrival_airport AND \
                arrival_airport =  if (\'{}\' = '', arrival_airport, \'{}\') AND \
                date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\') AND \
                date(arrival_time) =  if (\'{}\' = '', date(arrival_time), \'{}\') AND \
                airline_name = if (\'{}\' = '', airline_name, \'{}\') AND \
                price <= if (\'{}\' = '', price, \'{}\') \
            ORDER BY airline_name, flight_num
            """
        cursor.execute(query.format(
            departure_city, departure_city, departure_airport, departure_airport, 
            arrival_city, arrival_city, arrival_airport, arrival_airport, 
            departure_time, departure_time, arrival_time, arrival_time,
            airline_name, airline_name, price, price))
        data = cursor.fetchall()
        cursor.close()
        
        if data:
            return render_template('customerSearchFlight.html', email=email, username=username, upcoming_flights=data)
        else:
            error = 'Sorry! This flight is not in our database.'
            return render_template('customerSearchFlight.html', email=email, username=username, error1=error)
    
    else:
        session.clear()
        return render_template('404.html')

# (2) Customer Purchase New Tickets
@app.route('/customer/purchaseTickets', methods=['GET', 'POST'])
def customerPurchaseTicket():
    if session.get('email'):
        email = check_injection(session['email'])
        airline_name = check_injection(request.form['airline_name'])
        flight_num = request.form['flight_num']
        
        cursor = conn.cursor()
        query = "SELECT name FROM customer WHERE email = \'{}\'"
        cursor.execute(query.format(email))
        username = cursor.fetchone()
        username = str(username)[2:-3]
        cursor.close()
        
        cursor = conn.cursor()
        query2 = """
            SELECT * FROM flight \
            WHERE airline_name = \'{}\' AND flight_num = \'{}\' AND num_tickets_left > 0"""
        cursor.execute(query2.format(airline_name, flight_num))
        flight_data = cursor.fetchall()
        cursor.close()
    
        if flight_data:
            cursor = conn.cursor()
            query_id = "SELECT ticket_id FROM ticket ORDER BY ticket_id DESC LIMIT 1"
            cursor.execute(query_id)
            ticket_id_data = cursor.fetchone()
            new_ticket_id = int(ticket_id_data[0]) + 1
            insert1 = "INSERT INTO ticket VALUES (\'{}\', \'{}\', \'{}\')"
            cursor.execute(insert1.format(new_ticket_id, airline_name, flight_num))
            insert2 = "INSERT INTO purchase (ticket_id, customer_email, purchase_date) \
                        VALUES (\'{}\', \'{}\', CURDATE())"
            cursor.execute(insert2.format(new_ticket_id, email))
            conn.commit()
            cursor.close()
            message = 'Ticket bought successfully!'
            return render_template('customerSearchFlight.html', email=email, username=username, message=message)
        else:
            ticket_error = 'No more tickets left.'
            return render_template('customerSearchFlight.html', error2=ticket_error, email=email, username=username)
    
    else:
        session.clear()
        return render_template('404.html')

# 4. Customer Track Spending
# Default view will be :
# (1) total amount of money spent in the past year 
# (2) a bar chart showing month-wise money spent for last 6 months. 
# Customer will also have option to specify a range of dates to view total amount of money 
# spent within that range and a bar chart showing month-wise money spent within that range.
@app.route('/customer/spending', methods=['POST', 'GET'])
def customerTrackSpending():
    if session.get('email'):
        email = check_injection(session['email'])
        
        cursor = conn.cursor()
        query0 = "SELECT name FROM customer WHERE email = \'{}\'"
        cursor.execute(query0.format(email))
        username = cursor.fetchone()
        username = str(username)[2:-3]
        cursor.close()

		# (1) show total spending in the past year or specified duration
        duration = request.form.get("duration")
        if duration is None:
            duration = "365"
        
        cursor = conn.cursor()
        query = """
            SELECT SUM(price) \
            FROM customer_spending \
            WHERE customer_email = \'{}\' AND \
                (purchase_date BETWEEN DATE_ADD(NOW(), INTERVAL -\'{}\' DAY) and NOW())"""
        cursor.execute(query.format(email, duration))
        total_spending_data = cursor.fetchone()
        cursor.close()

		# (2) show month-wise spending in the past 6 months
        period = request.form.get("period")
        if period is None:
            period = "6"
        today = date.today()
        past_day = today.day
        past_month = (today.month - int(period)) % 12
        if past_month == 0:
            past_month = 12
        past_year = today.year + ((today.month - int(period) - 1) // 12)
        past_date = date(past_year, past_month, past_day)
        
        cursor = conn.cursor()
        query2 = """
            SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, \
                SUM(price) AS monthly_spending \
            FROM customer_spending \
            WHERE customer_email = \'{}\' AND purchase_date >= \'{}\' \
            GROUP BY YEAR(purchase_date), MONTH(purchase_date)"""
        cursor.execute(query2.format(email, past_date))
        monthly_spending_data = cursor.fetchall()
        cursor.close()

        months = []
        monthly_spendings = []
        for i in range(int(period)):
            month = (past_date.month+i+1)%12
            if month == 0:
                month = 12
            year = past_date.year + ((past_date.month+i)//12)
            flag = False
            for one_month in monthly_spending_data:
                if (one_month[0]==year) and (one_month[1]==month):
                    flag = True
                    break
            if flag:
                monthly_spendings.append(int(one_month[2]))
            else:
                monthly_spendings.append(0)
            months.append(str(year)+'/'+str(month))

        return render_template('customerSpending.html', email=email, username=username,
            total_spending_data=total_spending_data[0], duration=duration, period=period,
            months=months, monthly_spendings=monthly_spendings)
    
    else:
        session.clear()
        return render_template('404.html')

# ------- Booking Agent Exclusive Functions --------
# 0. Booking Agent Homepage
@app.route('/agent/home')
def homeAgent():
    if session.get('email'):
        email = check_injection(session['email'])
        return render_template('homeAgent.html', email=email, emailName=email.split('@')[0])
    else:
        session.clear()
        return render_template('404.html')

# 1. Booking Agent View Purchased Tickets
# Provide various ways for the booking agents to see flights information for which they 
# purchased on behalf of customers. The default should be showing for the upcoming flights. 
# Optionally you may include a way for the user to specify a range of dates, specify destination 
# and/or source airport and/or city etc to show all the flights for which they purchased.
@app.route('/agent/viewTickets', methods=['GET', 'POST'])
def agentViewTicket():
    if session.get('email'):
        email = check_injection(session['email'])
			
        cursor = conn.cursor()
        query1 = "SELECT booking_agent_id FROM bookingAgent WHERE email = \'{}\'"
        cursor.execute(query1.format(email))
        booking_agent_id = cursor.fetchone()
        query2 = "SELECT * FROM agent_view_flight WHERE email = \'{}\'"
        cursor.execute(query2.format(email))
        data = cursor.fetchall()
        cursor.close()
        return render_template('agentViewTicket.html', email=email, view_my_flights=data, booking_agent_id=booking_agent_id)
    
    else:
        session.clear()
        return render_template('404.html')

# 2.-3. Booking Agent Search Flight and Purchase Ticket
@app.route('/agent/search&purchase', methods=['GET', 'POST'])
def agentSearchPurchase():
    if session.get('email'):
        email = check_injection(session['email'])
        cursor = conn.cursor()
        query = "SELECT email FROM bookingAgent WHERE email = \'{}\'"
        cursor.execute(query.format(email))
        data = cursor.fetchall()
        cursor.close()
    return render_template('agentSearchFlight.html', posts=data)

# 2. Booking Agent Purchase New Ticket
@app.route('/agent/purchaseTickets', methods=['GET', 'POST'])
def agentPurchaseTicket():
    if session.get('email'):
        email = check_injection(session['email'])
        airline_name = check_injection(request.form.get("airline_name"))
        flight_num = request.form.get("flight_num")
        customer_email = check_injection(request.form['customer_email'])

		# validate booking agent email
        cursor = conn.cursor()
        query = "SELECT booking_agent_id FROM bookingAgent where email = \'{}\'"
        cursor.execute(query.format(email))
        agentData = cursor.fetchone()
        booking_agent_id = agentData[0]
        cursor.close()
        if not agentData:
            agent_id_error = 'You are not a booking agent.'
            return render_template('agentSearchFlight.html', error2=agent_id_error)

		# validate customer_email is registered
        cursor = conn.cursor()
        query2 = "SELECT * FROM customer WHERE email = \'{}\'"
        cursor.execute(query2.format(customer_email))
        customer_data = cursor.fetchone()
        cursor.close()
        if not customer_data:
            customer_error = 'Your customer is not registered.'
            return render_template('agentSearchFlight.html', error2=customer_error)

		# customer_email is validated
        cursor = conn.cursor()
        query3 = """
            SELECT * FROM flight \
            WHERE airline_name = \'{}\' AND flight_num = \'{}\' AND num_tickets_left > 0"""
        cursor.execute(query3.format(airline_name, flight_num))
        flight_data = cursor.fetchall()
        cursor.close()
        if not flight_data:
            ticket_error = 'No more tickets left.'
            return render_template('agentSearchFlight.html', error2=ticket_error, email=email, emailName=email.split('@')[0])
        else:
            cursor = conn.cursor()
            query4 = "SELECT ticket_id FROM ticket ORDER BY ticket_id DESC LIMIT 1"
            cursor.execute(query4)
            ticket_id_data = cursor.fetchone()
            new_ticket_id = int(ticket_id_data[0]) + 1
            insert1 = "INSERT INTO ticket VALUES (\'{}\', \'{}\', \'{}\')"
            cursor.execute(insert1.format(new_ticket_id, airline_name, flight_num))
            insert2 = "INSERT INTO purchase VALUES (\'{}\', \'{}\', \'{}\', \'{}\', CURDATE())"
            cursor.execute(insert2.format(new_ticket_id, customer_email, booking_agent_id, email))
            conn.commit()
            cursor.close()
            message = 'Ticket bought successfully!'
            return render_template('agentSearchFlight.html', message=message, email=email, emailName=email.split('@')[0])
    
    else:
        session.clear()
        return render_template('404.html')

# 3. Booking Agent Search Flights
@app.route('/agent/searchFlights', methods=['GET', 'POST'])
def agentSearchFlights():
    if session.get('email'):
        email = check_injection(session['email'])
        departure_city = check_injection(request.form['departure_city'])
        departure_airport = check_injection(request.form['departure_airport'])
        departure_time = request.form['departure_time']
        arrival_city = check_injection(request.form['arrival_city'])
        arrival_airport = check_injection(request.form['arrival_airport'])
        arrival_time = request.form['arrival_time']
        airline_name = request.form['airline_name']
        price = request.form['price']
        
        cursor = conn.cursor()
        query = "SELECT email from bookingAgent where email = \'{}\'"
        cursor.execute(query.format(email))
        agent_data = cursor.fetchone()
        cursor.close()
        
        if not agent_data:
            agent_id_error = 'You are not a booking agent.'
            return render_template('agentSearchFlight.html', error1=agent_id_error)
        
        cursor = conn.cursor()
        query = """
            SELECT airplane_id, flight_num, 
                Depart.airport_city, departure_airport, 
                Arrive.airport_city, arrival_airport, 
                departure_time, arrival_time, 
                status, price, airline_name, num_tickets_left \
            FROM airport AS Depart, flight, airport AS Arrive \
            WHERE Depart.airport_city = if (\'{}\' = '',Depart.airport_city, \'{}\') AND \
                Depart.airport_name = departure_airport AND \
                departure_airport = if (\'{}\' = '', departure_airport, \'{}\') AND \
                Arrive.airport_city = if (\'{}\' = '', Arrive.airport_city, \'{}\')AND \
                Arrive.airport_name = arrival_airport AND \
                arrival_airport =  if (\'{}\' = '', arrival_airport, \'{}\') AND \
                date(departure_time) = if (\'{}\' = '', date(departure_time), \'{}\') AND \
                date(arrival_time) =  if (\'{}\' = '', date(arrival_time), \'{}\') AND \
                airline_name = if (\'{}\' = '', airline_name, \'{}\') AND \
                price <= if (\'{}\' = '', price, \'{}\')
            ORDER BY airline_name, flight_num
            """
        cursor.execute(query.format(
            departure_city, departure_city, departure_airport, departure_airport, 
            arrival_city, arrival_city, arrival_airport, arrival_airport, 
            departure_time, departure_time, arrival_time, arrival_time,
            airline_name, airline_name, price, price))
        data = cursor.fetchall()
        cursor.close()
        
        if data:
            return render_template('agentSearchFlight.html', email=email, emailName=email.split('@')[0], upcoming_flights=data)
        else:
            error = 'Sorry! This flight is not in our database.'
            return render_template('agentSearchFlight.html', email=email, emailName=email.split('@')[0], error1=error)
    
    else:
        session.clear()
        return render_template('404.html')

# 4. Booking Agent View Commissions
# Default view will be total amount of commission received in the past 30 days 
# and the average commission they received per ticket booked in the past 30 days 
# and total number of tickets sold by them in the past 30 days. 
# They will also have option to specify a range of dates to view total amount of
# commission received and total numbers of tickets sold.
@app.route('/agent/commission', methods=['POST', 'GET'])
def agentCommission():
    if session.get('email'):
        email = check_injection(session['email'])
        duration = request.form.get("duration")

        # custom_duration = request.form.get("custom_duration")
        # if custom_duration is not None:
        #     custom_duration = custom_duration
        # query = """
        #     SELECT SUM(ticket_price * 0.1), AVG(ticket_price * 0.1), COUNT(ticket_price * 0.1) \
        #     FROM agent_commission 
        #     WHERE email = \'{}\' AND \
        #         (purchase_date BETWEEN DATE_ADD(NOW(), INTERVAL -\'{}\' DAY) and NOW())
        #     """
        # cursor = conn.cursor()  
        # cursor.execute(query.format(email, custom_duration))
        # commission_data = cursor.fetchone()
        # total_commission, avg_commission, num_ticket = commission_data
        # cursor.close()

        if duration is None:
            duration = "30"
        
        query = """
            SELECT SUM(ticket_price * 0.1), AVG(ticket_price * 0.1), COUNT(ticket_price * 0.1) \
            FROM agent_commission 
            WHERE email = \'{}\' AND \
                (purchase_date BETWEEN DATE_ADD(NOW(), INTERVAL -\'{}\' DAY) and NOW())"""
        cursor = conn.cursor()
        cursor.execute(query.format(email, duration))
        commission_data = cursor.fetchone()
        total_commission, avg_commission, num_ticket = commission_data
        cursor.close()
        
        return render_template('agentCommission.html', email=email, emailName=email.split('@')[0],
            total_commission=total_commission, avg_commission=avg_commission,
            num_ticket=num_ticket, duration=duration)#, custom_duration=custom_duration)
    
    else:
        session.clear()
        return render_template('404.html')

# 5. Booking Agent View Top Customers
# Top 5 customers based on number of tickets bought from the booking agent in the past 6 months 
# and top 5 customers based on amount of commission received in the last year. 
# Show a bar chart showing each of these 5 customers in x-axis and number of tickets bought in y-axis. 
# Show another bar chart showing each of these 5 customers in x-axis and amount commission received in y- axis.
@app.route('/agent/topCustomers')
def agentTopCustomers():
    if session.get('email'):
        email = check_injection(session['email'])

        # (1) by number of tickets (last 6 months)
        cursor = conn.cursor()
        query = """
            SELECT customer_email, COUNT(ticket_id) \
            FROM agent_commission 
            WHERE email = \'{}\' AND \
                DATEDIFF(CURDATE(), DATE(purchase_date)) < 183 \
            GROUP BY customer_email \
            ORDER BY COUNT(ticket_id) DESC"""
        cursor.execute(query.format(email))
        ticket_data = cursor.fetchall()
        cursor.close()

        l = len(ticket_data)
        if l >= 5:
            ppl1 = [ticket_data[i][0] for i in range(5)]
            tickets = [int(ticket_data[i][1]) for i in range(5)]
        else:
            ppl1 = [ticket_data[i][0] for i in range(l)]
            tickets = [int(ticket_data[i][1]) for i in range(l)]
            for _ in range(5 - l):
                ppl1.append(' ')
                tickets.append(0)
		
        # (2) by amount of commission (last year)
        cursor = conn.cursor()
        query2 = """
            SELECT customer_email, SUM(ticket_price)*0.1 \
            FROM agent_commission 
            WHERE email = \'{}\' AND \
                DATEDIFF(CURDATE(), DATE(purchase_date)) < 365 \
            GROUP BY customer_email \
            ORDER BY SUM(ticket_price) DESC"""
        cursor.execute(query2.format(email))
        commission_data = cursor.fetchall()
        cursor.close()


        l2 = len(commission_data)
        if l2 >= 5:
            ppl2 = [commission_data[i][0] for i in range(5)]
            commissions = [int(commission_data[i][1]) for i in range(5)]
        else:
            ppl2 = [commission_data[i][0] for i in range(l2)]
            commissions = [int(commission_data[i][1]) for i in range(l2)]
            for _ in range(5 - l):
                ppl2.append(' ')
                commissions.append(0)

        return render_template('agentTopCustomers.html', email=email, emailName=email.split('@')[0],
            ppl1=ppl1, ppl2=ppl2, tickets=tickets, commissions=commissions)
    
    else:
        session.clear()
        return render_template('404.html')


# ------ Airline Staff Exclusive Functions -------
# 0. Staff Homepage
@app.route('/staff/home')
def homeStaff():
    if session.get('username'):
        username = check_injection(session['username'])
        cursor = conn.cursor()
        query = """
            SELECT ticket_id, airline_name, airplane_id, flight_num, A1.airport_city, 
            departure_airport, A2.airport_city, arrival_airport, departure_time, arrival_time, status \
            FROM flight NATURAL JOIN purchase NATURAL JOIN ticket, airport AS A2, airport AS A1\
            WHERE customer_email = \'{}\' AND status = 'upcoming' AND \
            A2.airport_name = departure_airport AND A1.airport_name = arrival_airport"""
        cursor.execute(query.format(username))
        data = cursor.fetchall() 
        cursor.close()
        return render_template('homeStaff.html', username=username.split('@')[0], view_my_flights=data)
    else:
        session.clear()
        return render_template('404.html')


# 1. Airline Staff View Airline Flights
# Defaults will be showing all the upcoming flights operated by the airline they work for the next 30 days. 
# They will be able to see all the current/future/past flights operated by the airline they work for 
# based on range of dates, source/destination airports/city etc. 
# They will be able to see all the customers of a particular flight.
@app.route('/staff/flight/viewFlight', methods=['GET', 'POST'])
def staffViewFlights():
    if session.get('username'):
        username = check_injection(session['username'])
        
        cursor = conn.cursor()
        query = """
            SELECT username, airline_name, airplane_id, flight_num, \
                departure_airport, arrival_airport, departure_time, arrival_time \
            FROM flight NATURAL JOIN airlineStaff \
            WHERE username = \'{}\' and status = 'upcoming' and DATEDIFF(CURDATE(), DATE(departure_time))<30 
            """
        cursor.execute(query.format(username))
        data1 = cursor.fetchall()
        cursor.close()
        return render_template('staffViewFlight.html', username=username, posts=data1)
    else:
        session.clear()
        return render_template('404.html')

# 2.-5. Airline Staff Edit Flight Data
@app.route('/staff/flight/editFlightData', methods=['GET', 'POST'])
def editFlightData():
    if session.get('username'):
        username = check_injection(session['username'])
        cursor = conn.cursor()
        query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
        cursor.execute(query.format(username))
        data = cursor.fetchall()
        cursor.close()
    return render_template('staffEditFlightData.html', posts=data)

# 2. Airline Staff Change Flight Status
@app.route('/staff/flight/editStatus', methods=['GET', 'POST'])
def editFlightStatus():
    if session.get('username'):
        username = check_injection(session['username'])
        status = request.form['edit_status']
        flight_num = request.form['flight_num']
        
        cursor = conn.cursor()
        update = "UPDATE flight SET status = \'{}\' WHERE flight_num = \'{}\'"
        cursor.execute(update.format(status, flight_num))
        conn.commit()
        
        query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
        cursor.execute(query.format(username))
        data = cursor.fetchall()
        cursor.close()
        
        message = 'Flight status changed successfully.'
        return render_template('staffEditFlightData.html', username=username, message=message, posts=data)
    
    else:
        session.clear()
        return render_template('404.html')

# 3. Airline Staff Add New Flight
@app.route('/staff/flight/addFlight', methods=['GET', 'POST'])
def addFlight():
    if session.get('username'):
        username = check_injection(session['username'])
        
        flight_num = request.form['flight_num']
        departure_airport = check_injection(request.form['departure_airport'])
        departure_time = request.form['departure_time']
        arrival_airport = check_injection(request.form['arrival_airport'])
        arrival_time = request.form['arrival_time']
        price = request.form['price']
        seats = request.form['seats']
        status = request.form['status']
        airplane_id = request.form['airplane_id']

        cursor = conn.cursor()
        query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
        cursor.execute(query.format(username))
        data2 = cursor.fetchall()
        
        airline = "SELECT airline_name FROM airlineStaff WHERE username = \'{}\'"
        cursor.execute(airline.format(username))
        airline_name = cursor.fetchone()
        airline_name = airline_name[0]
        
        query = "SELECT airport_name FROM airport WHERE airport_name = \'{}\'"
        cursor.execute(query.format(departure_airport))
        data = cursor.fetchall()
        error1 = None
        
        if not data:
            error1 = "This departure airport doesn't exist."
            query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airlineStaff WHERE username = \'{}\'"
            cursor.execute(query.format(username))
            data1 = cursor.fetchall()
            return render_template('staffEditFlightData.html', error1=error1, username=username, airplane=data1, posts=data2)
        
        query = "SELECT airport_name FROM airport WHERE airport_name = \'{}\'"
        cursor.execute(query.format(arrival_airport))
        data = cursor.fetchall()
        error1 = None
        if not data:
            error1 = "This arrival airport doesn't exist."
            query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airlineStaff WHERE username = \'{}\'"
            cursor.execute(query.format(username))
            data1 = cursor.fetchall()
            return render_template('staffEditFlightData.html', error1=error1, username=username, airplane=data1, posts=data2)
            
        query = "SELECT airplane_id FROM airplane WHERE airline_name = \'{}\' and airplane_id = \'{}\'"
        cursor.execute(query.format(airline_name, airplane_id))
        data = cursor.fetchall()
        error1 = None
        if not data:
            error1 = "This airplane doesn't exist."
            query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airlineStaff WHERE username = \'{}\'"
            cursor.execute(query.format(username))
            data1 = cursor.fetchall()
            return render_template('staffEditFlightData.html', error1=error1, username=username, airplane=data1, posts=data2)

        num = "SELECT seats FROM airplane NATURAL JOIN airlineStaff WHERE username = \'{}\' and airplane_id = \'{}\'"
        cursor.execute(num.format(username, airplane_id))
        num = cursor.fetchone()
        if int(seats) >= int(num[0]):
            num_error = "The number of seats left cannot be more than the airplane seats."
            query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airlineStaff WHERE username = \'{}\'"
            cursor.execute(query.format(username))
            data1 = cursor.fetchall()
            return render_template('staffEditFlightData.html', error1=num_error, username=username, airplane=data1, posts=data2)
        
        query = "SELECT airline_name, flight_num FROM flight WHERE airline_name = \'{}\' and flight_num = \'{}\'"
        cursor.execute(query.format(airline_name, flight_num))
        data = cursor.fetchone()
        error1 = None
        if data:
            error1 = "This flight already exists."
            query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airlineStaff WHERE username = \'{}\'"
            cursor.execute(query.format(username))
            data1 = cursor.fetchall()
            cursor.close()
            return render_template('staffEditFlightData.html', error1=error1, username=username, airplane=data1, posts=data2)		
        
        else:
            insert = "INSERT INTO flight VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
            cursor.execute(insert.format(airline_name, flight_num, 
                                        departure_airport, departure_time, 
                                        arrival_airport, arrival_time, 
                                        price, status, airplane_id, seats))
            conn.commit()
            query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airlineStaff WHERE username = \'{}\'"
            cursor.execute(query.format(username))
            data1 = cursor.fetchall()
            cursor.close()
            message1 = "New flight successfully added."
            return render_template('staffEditFlightData.html', message1=message1, username=username, airplane=data1, posts=data2)
    
    else:
        session.clear()
        return render_template('404.html')

# 4. Airline Staff Add New Airplane
@app.route('/staff/flight/addAirplane', methods=['GET', 'POST'])
def addAirplane():
    if session.get('username'):
        username = check_injection(session['username'])
        airplane_id = request.form['airplane_id']
        seats = request.form['seats']
        
        cursor = conn.cursor()
        query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
        cursor.execute(query.format(username))
        data2 = cursor.fetchall()
        
        airline = "SELECT airline_name FROM airlineStaff WHERE username = \'{}\'"
        cursor.execute(airline.format(username))
        
        airline_name = cursor.fetchone()
        airline_name = airline_name[0]
        query = "SELECT airline_name, airplane_id FROM airplane WHERE airline_name = \'{}\' and airplane_id = \'{}\'"
        cursor.execute(query.format(airline_name, airplane_id))
        data = cursor.fetchone()
        error2 = None
        if data:
            error2 = "This airplane already exists."
            query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airlineStaff WHERE username = \'{}\'"
            cursor.execute(query.format(username))
            data1 = cursor.fetchall()
            cursor.close()
            return render_template('staffEditFlightData.html', error2=error2, username=username, airplane=data1, posts=data2)
        else:
            insert = "INSERT INTO airplane VALUES(\'{}\', \'{}\', \'{}\')"
            cursor.execute(insert.format(airline_name, airplane_id, seats))
            query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airlineStaff WHERE username = \'{}\'"
            cursor.execute(query.format(username))
            data1 = cursor.fetchall()
            conn.commit()
            cursor.close()
            message2 = "New airplane successfully added."
            return render_template('staffEditFlightData.html', message2=message2, username=username, airplane=data1, posts=data2)
    
    else:
        session.clear()
        return render_template('404.html')

# 5. Airline Staff Add Airport
@app.route('/staff/flight/addAirport', methods=['GET', 'POST'])
def addAirport():
	if session.get('username'):
		username = check_injection(session['username'])
		airport_name = check_injection(request.form['airport_name'])
		airport_city = check_injection(request.form['airport_city'])

		cursor = conn.cursor()
		query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data2 = cursor.fetchall()

		airport = "SELECT airport_name FROM airport WHERE airport_name = \'{}\'"
		cursor.execute(airport.format(airport_name))
		airport_data = cursor.fetchone()
		query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airlineStaff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data1 = cursor.fetchall()
		cursor.close()

		error3 = None
		if airport_data:
			error3 = "This airport already exists."
			return render_template('staffEditFlightData.html', error3=error3, username=username, airplane=data1, posts=data2)

		else:
			cursor = conn.cursor()
			insert = "INSERT INTO airport VALUES(\'{}\', \'{}\')"
			cursor.execute(insert.format(airport_name, airport_city))
			conn.commit()
			cursor.close()
			message3 = "New airport successfully added."
			return render_template('staffEditFlightData.html', message3=message3, username=username, airplane=data1, posts=data2)
	else:
		session.clear()
		return render_template('404.html')

# 6. Airline Staff View Booking Agents 
# Top 5 booking agents based on number of tickets sales for the past month and past year. 
# Top 5 booking agents based on the amount of commission received for the last year.
@app.route('/staff/agents')
def staffTopAgent():
	if session.get('username'):
		username = check_injection(session['username'])
		cursor = conn.cursor()

		query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		agentData = cursor.fetchall()

		query1 = """
            SELECT email, booking_agent_id, SUM(price)*0.1 AS commission \
            FROM bookingAgent NATURAL JOIN purchase \
                NATURAL JOIN flight NATURAL JOIN ticket AS T, airlineStaff \
            WHERE username = \'{}\' AND airlineStaff.airline_name = T.airline_name \
                AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 365  \
            GROUP BY email, booking_agent_id \
            ORDER BY commission DESC \
            LIMIT 5
            """
		cursor.execute(query1.format(username))
		data1 = cursor.fetchall()

		query2 = """
            SELECT bookingAgent.email, booking_agent_id, COUNT(ticket_id) AS ticket \
            FROM bookingAgent NATURAL JOIN purchase NATURAL JOIN ticket AS T, airlineStaff \
			WHERE username = \'{}\' AND airlineStaff.airline_name = T.airline_name \
                AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 30 \
			GROUP BY email, booking_agent_id \
			ORDER BY ticket DESC \
            LIMIT 5 
            """
		cursor.execute(query2.format(username))
		data2 = cursor.fetchall()

		query3 = """
            SELECT email, booking_agent_id, COUNT(ticket_id) AS ticket \
            FROM bookingAgent NATURAL JOIN purchase NATURAL JOIN ticket AS T, airlineStaff \
			WHERE username = \'{}\' and airlineStaff.airline_name = T.airline_name \
                AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 365 \
			GROUP BY email, booking_agent_id \
			ORDER BY ticket DESC \
            LIMIT 5 
            """
		cursor.execute(query3.format(username))
		data3 = cursor.fetchall()

		query = "SELECT email, booking_agent_id FROM bookingAgent"
		cursor.execute(query)
		data = cursor.fetchall()
		cursor.close()
		return render_template('staffAgent.html', username=username, commission=data1, month=data2, year=data3, posts=data, agentData=agentData)
	else:
		session.clear()
		return render_template('404.html')

# 7. Airline Staff View Frequent Customers
# (1) Airline Staff will also be able to see the most frequent customer within the last year. 
@app.route('/staff/customer', methods=['GET', 'POST'])
def staffTopCustomer():
	if session.get('username'):
		username = check_injection(session['username'])
		cursor = conn.cursor()
		query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data2 = cursor.fetchall()

		query1 = """
            SELECT email, name, COUNT(ticket_id) AS ticket \
            FROM customer, purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
			WHERE email = customer_email AND username = \'{}\' AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 365 \
			GROUP BY email, name \
			ORDER BY ticket \
            DESC LIMIT 1
            """
		cursor.execute(query1.format(username))
		data1 = cursor.fetchall()
		cursor.close()
		return render_template('staffCustomer.html', frequent=data1, username=username, customerData=data2)
	else:
		session.clear()
		return render_template('404.html')

# (2) Airline Staff will be able to see a list of all flights a particular Customer has taken on that airline.
@app.route('/staff/customer/customerFlights', methods=['GET', 'POST'])
def staffCustomerFlight():
	if session.get('username'):
		username = check_injection(session['username'])
		email = check_injection(request.form['customer_email'])

		cursor = conn.cursor()
		query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		customerData = cursor.fetchall()

		query2 = """
            SELECT DISTINCT airplane_id, flight_num, departure_airport, arrival_airport, \
                departure_time, arrival_time, status \
            FROM customer, purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
                WHERE email = \'{}\' and email = customer_email and username = \'{}\'"""
		cursor.execute(query2.format(email, username))
		data2 = cursor.fetchall()

		query1 = """
            SELECT email, name, COUNT(ticket_id) AS ticket \
            FROM customer, purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
			WHERE email = customer_email AND username = \'{}\' \
                AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 365\
			GROUP BY email, name \
			ORDER BY ticket \
            DESC LIMIT 1
            """
		cursor.execute(query1.format(username))
		data1 = cursor.fetchall()
		cursor.close()

		error = None
		if data2:
			return render_template('staffCustomer.html', customerFlights=data2, frequent=data1, username=username, customerData=customerData)
		else:
			cursor = conn.cursor()
			cus = "SELECT email FROM customer WHERE email = \'{}\'"
			cursor.execute(cus.format(email))
			cus = cursor.fetchone()
			cursor.close()
			if cus:
				error = "This customer didn't take any flight from us."
			else:
				error = "This customer doesn't exist."
			return render_template('staffCustomer.html', error=error, frequent=data1, username=username, customerData=customerData)
	else:
		session.clear()
		return render_template('404.html')

# (3) Airline Staff will be able to see a list of Customers a particular Flight has on that airline.
@app.route('/staff/customer/flightCustomers', methods=['GET', 'POST'])
def staffFlightCustomer():
	if session.get('username'):
		username = check_injection(session['username'])
		flight_num = request.form['flight_num']

		cursor = conn.cursor()
		cursor = conn.cursor()
		query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		customerData = cursor.fetchall()

		query3 = """
            SELECT DISTINCT email, name 
            FROM customer, purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff\
            WHERE flight_num = \'{}\' and email = customer_email and username = \'{}\'
            """
		cursor.execute(query3.format(flight_num, username))
		data3 = cursor.fetchall()

		query1 = """
            SELECT email, name, COUNT(ticket_id) AS ticket 
            FROM customer, purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
            WHERE email = customer_email AND username = \'{}\' and DATEDIFF(CURDATE(), DATE(purchase_date)) < 365\
            GROUP BY email, name\
            ORDER BY ticket DESC 
            LIMIT 1
            """
		cursor.execute(query1.format(username))
		data1 = cursor.fetchall()

		cursor.close()
		error3 = None
		if data3:
			return render_template('staffCustomer.html', flightCustomers = data3, frequent = data1, username = username, customerData = customerData)
		else:
			cursor = conn.cursor()
			cus = "SELECT flight_num FROM flight NATURAL JOIN airline_staff WHERE flight_num = \'{}\'\
				AND username = \'{}\'"
			cursor.execute(cus.format(flight_num, username))
			cus = cursor.fetchone()
			cursor.close()
			if(cus):
				error3 = "This flight has no customers."
			else:
				error3 = 'No such flight exists.'
			return render_template('staffCustomer.html', error3 = error3, frequent = data1, username = username, customerData = customerData)
	else:
		session.clear()
		return render_template('404.html')

# 8. Airline Staff View Ticket Reports 
# Total amounts of ticket sold based on range of dates/last year/last month etc. 
# Month-wise tickets sold in a bar chart.
@app.route('/staff/ticketReport')
def staffTicketReport():
	if session.get('username'):
		username = check_injection(session['username'])
		cursor = conn.cursor()
		query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
		cursor.execute(query.format(username))
		data2 = cursor.fetchall()
		cursor.close()
		return render_template('staffTicketReport.html', username=username, posts=data2)
	else:
		session.clear()
		return render_template('404.html')

@app.route('/staff/ticket', methods=['GET', 'POST'])
def staffTicket():
    if session.get('username'):
        username = check_injection(session['username'])
        start = request.form['start']
        end = request.form['end']
        query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
        cursor = conn.cursor()
        cursor.execute(query.format(username))
        data2 = cursor.fetchall()
        
        ticket = """
            SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, count(ticket_id) FROM \
            purchase NATURAL JOIN airlineStaff NATURAL JOIN flight NATURAL JOIN ticket\
            WHERE purchase_date > \'{}\'\
            and purchase_date < \'{}\' AND username = \'{}\' \
            GROUP BY year, month\
            ORDER BY year, month
            """
        cursor.execute(ticket.format(start, end, username))
        allTickets = cursor.fetchall()
        cursor.close()
        
        startYear = allTickets[0][0]
        startMonth = allTickets[0][1]
        endYear = allTickets[-1][0]
        endMonth = allTickets[-1][1]
        if startYear == endYear:
            period = endMonth - startMonth + 1
        else:
            period = 12*(endYear-startYear-1) + endMonth + (12-startMonth+1)
        
        startDate = str(startYear)+'/'+str(startMonth)
        endDate = str(endYear)+'/'+str(endMonth)

        if allTickets:
            time = []
            monthTickets = []
            for i in range(int(period)):
                month = (startMonth+i+1)%12
                if month == 0:
                    month = 12
                year = startYear + ((startMonth+1)//12)
                flag = False
                for one_month in allTickets:
                    if (one_month[0]==year) and (one_month[1]==month):
                        flag = True
                        break
                if flag:
                    monthTickets.append(int(one_month[2]))
                else:
                    monthTickets.append(0)
                time.append(str(year)+'/'+str(month))
            totalTickets = sum(monthTickets)
        
            return render_template('staffTicketReport.html', ticket=allTickets, 
                startDate=startDate, endDate=endDate, time=time, 
                totalTickets=totalTickets, monthTickets=monthTickets, 
                username=username, posts=data2)
        
        else:
            error = "No tickets sold."
            return render_template('staffTicketReport.html', error=error, username=username, posts=data2)
    
    else:
        session.clear()
        return render_template('404.html')

# 9. Airline Staff Revenue Comparison
# Draw a pie chart for showing total amount of revenue earned from direct sales 
# (when customer bought tickets without using a booking agent) and total amount 
# of revenue earned from indirect sales (when customer bought tickets using 
# booking agents) in the last month and last year
@app.route('/staff/earningsReport')
def staffEarningsReport():
    if session.get('username'):
        username = check_injection(session['username'])
        
        cursor = conn.cursor()
        query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
        cursor.execute(query.format(username))
        data2 = cursor.fetchall()
        
        query3 = """
            SELECT SUM(price)\
            FROM purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
            WHERE username = \'{}\' AND booking_agent_id IS NULL \
                AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 30 \
            GROUP BY airline_name
            """
        cursor.execute(query3.format(username))
        mdirect = cursor.fetchall()
        if mdirect:
            mdirect = [int(mdirect[0][0])]
        else:
            mdirect = [0]
            
        query4 = """
            SELECT SUM(price)\
            FROM purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
            WHERE username = \'{}\' AND booking_agent_id IS NOT NULL \
                AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 30 \
            GROUP BY airline_name
            """
        cursor.execute(query4.format(username))
        mindirect = cursor.fetchall()
        if(mindirect):
            mindirect = [int(mindirect[0][0])]
        else:
            mindirect = [0]
        
        query5 = """
            SELECT SUM(price) \
            FROM purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
            WHERE username = \'{}\' AND booking_agent_id IS NULL \
                AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 365\
            GROUP BY airline_name
            """
        cursor.execute(query5.format(username))
        ydirect = cursor.fetchall()
        if(ydirect):
            ydirect = [int(ydirect[0][0])]
        else:
            ydirect = [0]
        
        query6 = """
            SELECT SUM(price)\
            FROM purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
            WHERE username = \'{}\' AND booking_agent_id IS NOT NULL \
                AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 365 \
            GROUP BY airline_name
            """
        cursor.execute(query6.format(username))
        yindirect = cursor.fetchall()
        if yindirect:
            yindirect = [int(yindirect[0][0])]
        else:
            yindirect = [0]
        cursor.close()
        return render_template('staffRevenue.html', username=username, \
            mdirect=mdirect, mindirect=mindirect, ydirect=ydirect, yindirect=yindirect, posts=data2)
    else:
        session.clear()
        return render_template('404.html')

# 10. Airline Staff View Top Destinations 
# Find the top 3 most popular destinations for last 3 months and last year.
@app.route('/staff/topDestinations')
def staffTopDestinations():
    if session.get('username'):
        username = check_injection(session['username'])
        
        cursor = conn.cursor()
        query = "SELECT airline_name FROM airlineStaff WHERE username = \'{}\'"
        cursor.execute(query.format(username))
        airline = str(cursor.fetchone())[2:-3]
        
        query1 = """
            SELECT airport_city, count(ticket_id) AS ticket \
            FROM purchase NATURAL JOIN ticket NATURAL JOIN flight, airport \
            WHERE airport_name = arrival_airport AND \
                DATEDIFF(CURDATE(), DATE(purchase_date)) < 90 \
            GROUP BY airport_city \
            ORDER BY ticket DESC \
            LIMIT 3
            """
        cursor.execute(query1)
        monthData = cursor.fetchall()
        for column in monthData:
            monthDest = column[0]
            monthTickets = column[1]

        query2 = """
            SELECT airport_city, COUNT(ticket_id) AS ticket \
            FROM purchase NATURAL JOIN ticket NATURAL JOIN flight, airport \
            WHERE airport_name = arrival_airport \
                AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 365\
            GROUP BY airport_city \
            ORDER BY ticket DESC \
            LIMIT 3
            """
        cursor.execute(query2)
        yearData = cursor.fetchall()
        for column in yearData:
            yearDest = column[0]
            yearTickets = column[1]
        cursor.close()
		
        return render_template('staffTopDestination.html', 
            monthData=monthData, monthDest=monthDest, monthTickets=monthTickets,
            yearData=yearData, yearDest=yearDest, yearTickets=yearTickets,
            username=username, airline=airline)
    
    else:
        session.clear()
        return render_template('404.html')


# ------- Run app ----------
app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
