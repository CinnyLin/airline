# app.py

## Public Information
1. **search flight information**: using dates, departure cities/airports, airlines, or prices
    1. `app.py`: searchFlight()
    2. `templates`: index.html, publicSearchFlights.html
```
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
```
2. **search flight statuses**: based on airline name, flight number, or ticket id
    1. `app.py`: searchFlightStatus()
    2. `templates`: index.html, publicSearchFlightStatus.html
```
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
```

## Common User Functions
Three types of users: customers, booking agents, airline staffs
1. **register**: users can sign up as either types of users; quotation marks in input would be escaped
    1. `app.py`: registerAgent(), registerCustomer(), registerStaff(), registerAgentAuth(), registerCustomerAuth(), registerStaffAuth()
    2. `templates`: registerAgent.html, registerCustomer.html, registerStaff.html

2. **login**: when users login they would not have access to pages of other users
    1. `app.py`: login(), loginAgent(), loginCustomer(), loginStaff(), loginAgentAuth(), loginCustomerAuth(), loginStaffAuth()
    2. `templates`: login.html, loginAgent.html, loginCustomer.html, loginStaff.html
```
query = "SELECT * FROM customer WHERE email = \'{}\'"
query = "SELECT * FROM bookingAgent WHERE email = \'{}\'"
query = "SELECT * FROM airlineStaff WHERE username = \'{}\'"
```

3. **delete account**: users would be required to authenticate their email and password before deleting their account; with SQL ON DELETE CASCADE, their personal data would be deleted but anonymous purchase history would be kept
    1. `app.py`: deleteAccountAgent(), deleteAccountCustomer(), deleteAccountStaff(), deleteAccountAgentAuth(), deleteAccountCustomerAuth(), deleteAccountStaffAuth()
    2. `templates`: deleteAgent.html, deleteCustomer.html, deleteStaff.html
```
query = "DELETE FROM customer WHERE email = \'{}\' and password = md5(\'{}\')"
query = "DELETE FROM bookingAgent WHERE email = \'{}\' and password = md5(\'{}\')"
query = "DELETE FROM airlineStaff WHERE username = \'{}\' and password = md5(\'{}\')"
```

4. **reset password**: users would be required to authenticate their email and password before resetting their password, and would be redirected to login again
    1. `app.py`: resetAgent(), resetCustomer(), resetStaff()
    2. `templates`: resetAgent.html, resetCustomer.html, resetStaff.html
```
query = """
        UPDATE customer
        SET password = md5(\'{}\')
        WHERE email = \'{}\' AND password = md5(\'{}\')"""
query = """
        UPDATE bookingAgent
        SET password = md5(\'{}\')
        WHERE email = \'{}\' AND password = md5(\'{}\')
        """
query = """
        UPDATE airlineStaff
        SET password = md5(\'{}\')
        WHERE email = \'{}\' AND password = md5(\'{}\')
        """
```

5. **logout**: users would be logged out
    1. `app.py`: logout()

## Customer Exclusive Functions
1. **view tickets**: Platform provides various ways for the user to see flights information of tickets which they purchased.
    1. `customerViewTickets()` shows upcoming flights as default.
```
query = """
        SELECT ticket_id, airline_name, flight_num, 
        Depart.airport_city, departure_airport, Arrive.airport_city, arrival_airport, 
        departure_time, arrival_time, status \
        FROM flight NATURAL JOIN purchase NATURAL JOIN ticket, \
            airport AS Arrive, airport AS Depart\
        WHERE customer_email = \'{}\' AND status = 'upcoming' AND \
        Depart.airport_name = departure_airport AND Arrive.airport_name = arrival_airport
        """
```

2. **search and purchase flights**: Customer searches for upcoming flights based on city/airport, date etc. and purchase tickets for this flight.
    1. `customerSearchPurchase()`: renders the search/purchase front page
    2. `customerSearchFlights()`: sends search request to back-end and render search results to front-end
    3. `customerPurchaseTicket()`: pass search request to purchase function and pass to front-end
```
# search
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

# purchase
query2 = """
        SELECT * FROM flight \
        WHERE airline_name = \'{}\' AND flight_num = \'{}\' AND num_tickets_left > 0
        """
insert1 = "INSERT INTO ticket VALUES (\'{}\', \'{}\', \'{}\')"
insert2 = "INSERT INTO purchase (ticket_id, customer_email, purchase_date) \
            VALUES (\'{}\', \'{}\', CURDATE())"
```


3. **track spendings**: Customer can see total amount of money spent and montly spendings breakdown for a selected period of time.
    1. `customerTrackSpending()`: default view shows total amount of money spent in the past year and a bar chart showing month-wise money spending for the last 6 months.
```
# total spending
query = """
        SELECT SUM(price) \
        FROM customer_spending \
        WHERE customer_email = \'{}\' AND \
            (purchase_date BETWEEN DATE_ADD(NOW(), INTERVAL -\'{}\' DAY) and NOW())
        """

# month-wise spending
query2 = """
        SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, \
            SUM(price) AS monthly_spending \
        FROM customer_spending \
        WHERE customer_email = \'{}\' AND purchase_date >= \'{}\' \
        GROUP BY YEAR(purchase_date), MONTH(purchase_date)
        """
```

## Booking Agent Exclusive Functions
1. **view tickets**: Agent can see the flights information of tickets that they purchased on behalf of their customers. 
    1. `agentViewTicket()`: default shows upcoming flights.
```
query1 = "SELECT booking_agent_id FROM bookingAgent WHERE email = \'{}\'"
query2 = "SELECT * FROM agent_view_flight WHERE email = \'{}\'"
```

2. **search and purchase flights**: Agent searches for upcoming flights based on city/airport, date etc. and purchase tickets for this flight on behalf of customers.
    1. `agentSearchPurchase()`: renders the search/purchase front page
    2. `agentSearchFlights()`: sends search request to back-end and render search results to front-end
    3. `agentPurchaseTicket()`: pass search request to purchase function and pass to front-end; agent would have to enter the customer email to purchase on their behalf
```
# search
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

# purchase
query = "SELECT booking_agent_id FROM bookingAgent where email = \'{}\'"
query2 = "SELECT * FROM customer WHERE email = \'{}\'"
query3 = """
        SELECT * FROM flight \
        WHERE airline_name = \'{}\' AND flight_num = \'{}\' AND num_tickets_left > 0"""
query4 = "SELECT ticket_id FROM ticket ORDER BY ticket_id DESC LIMIT 1"
```

3. **view commission**: Agent can see total amount of commission received, average commission per ticket, and number of tickets booked for a selected period of time.
    1. `agentCommission()`: default view shows the results from the past month.
```
query = """
        SELECT SUM(ticket_price * 0.1), AVG(ticket_price * 0.1), COUNT(ticket_price * 0.1) \
        FROM agent_commission 
        WHERE email = \'{}\' AND \
            (purchase_date BETWEEN DATE_ADD(NOW(), INTERVAL -\'{}\' DAY) and NOW())
        """
```

4. **top customers**: Agent can see the top 5 customers based on number of tickets bought from the booking agent in the past 6 months and the top 5 customers based on amount of commission received in the last year.
```
# by number of tickets last 6 months
query = """
        SELECT customer_email, COUNT(ticket_id) \
        FROM agent_commission 
        WHERE email = \'{}\' AND \
            DATEDIFF(CURDATE(), DATE(purchase_date)) < 183 \
        GROUP BY customer_email \
        ORDER BY COUNT(ticket_id) DESC
        """

# by amount of commission last year
query2 = """
        SELECT customer_email, SUM(ticket_price)*0.1 \
        FROM agent_commission 
        WHERE email = \'{}\' AND \
            DATEDIFF(CURDATE(), DATE(purchase_date)) < 365 \
        GROUP BY customer_email \
        ORDER BY SUM(ticket_price) DESC
        """
```

## Airline Staff Exclusive Functions
1. **view flights**: Staff can see the flights information operated by their airline.
    1. `staffViewFlights()`: default shows all upcoming flights for their airline in the next 30 days.
```
query = """
        SELECT username, airline_name, airplane_id, flight_num, \
            departure_airport, arrival_airport, departure_time, arrival_time \
        FROM flight NATURAL JOIN airlineStaff \
        WHERE username = \'{}\' and status = 'upcoming' and DATEDIFF(CURDATE(), DATE(departure_time))<30 
        """
```

2. **edit flight data**: Staff can change flight information within their airline.
    1. `editFlightData()`: renders the front page where staffs can do all the edit data operations
    2. `editFlightStatus()`: allows staff to change flight status (from upcoming to in progress, in progress to delayed etc).
    3. `addFlight()`: staff can create a new flight by providing flight number, airplane id, departure/arrival time and airport, flight price,  flight status, and seats (i.e. number of tickets left). 
    **Note1**: Here it would check if the "number of tickets left (`flight.num_tickets_left`)" is less than or equal to "the number of seats of the airplane" (`airplane.seats`).
    **Note2**: `num_tickets_left` is a new column we added in the `flight` table in order to check if there is still tickets left when customers/agents make their flight purchases.
    4. `addAirplane()`: staff can create a new airplane for their airline by providing airplane id and number of seats that airplane has.
    5. `addAirport()`: staff can create a new airport by providing the airport name and airport city.
    6. Each function checks if the added information is already in our database system. It returns appropriate messages after an edit, such as an error message saying that the airport already exists.
    7. The application prevents unauthorizaed users from doing these actions by checking the session of the user in each operation (`if session.get('username')`) and separating the routing path of all users (`/staff/[editFlightDataOperation]`)
```
# edit flight status
update = "UPDATE flight SET status = \'{}\' WHERE flight_num = \'{}\'"
query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"

# add new flight
query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
airline = "SELECT airline_name FROM airlineStaff WHERE username = \'{}\'"
airport = "SELECT airport_name FROM airport WHERE airport_name = \'{}\'" #check that airport exists
airplane = "SELECT airplane_id FROM airplane WHERE airline_name = \'{}\' and airplane_id = \'{}\'"
num = "SELECT seats FROM airplane NATURAL JOIN airlineStaff WHERE username = \'{}\' and airplane_id = \'{}\'" # check that tickets left <= seats provided
query = "SELECT airline_name, flight_num FROM flight WHERE airline_name = \'{}\' and flight_num = \'{}\'"
insert = "INSERT INTO flight VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"

# add new airplane
query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
airline = "SELECT airline_name FROM airlineStaff WHERE username = \'{}\'"
query = "SELECT airline_name, airplane_id FROM airplane WHERE airline_name = \'{}\' and airplane_id = \'{}\'" # check that airplane already exists
insert = "INSERT INTO airplane VALUES(\'{}\', \'{}\', \'{}\')"

# add new airport
query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
airport = "SELECT airport_name FROM airport WHERE airport_name = \'{}\'" # check that airport already exists
query = "SELECT airplane_id, seats FROM airplane NATURAL JOIN airlineStaff WHERE username = \'{}\'"
insert = "INSERT INTO airport VALUES(\'{}\', \'{}\')"
```

3. **booking agent**: Staff can see top 5 booking agents based on the number of tickets they sold and the amount of commission they received.
    1. `staffTopAgent()`: default shows number of tickets sold for the past month, and amount of commission received the last year.
```
# by number of tickets sold last month and last year 
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

# by amount of commission received last year
query2 = """
        SELECT bookingAgent.email, booking_agent_id, COUNT(ticket_id) AS ticket \
        FROM bookingAgent NATURAL JOIN purchase NATURAL JOIN ticket AS T, airlineStaff \
        WHERE username = \'{}\' AND airlineStaff.airline_name = T.airline_name \
            AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 30 \
        GROUP BY email, booking_agent_id \
        ORDER BY ticket DESC \
        LIMIT 5 
        """
```

4. **customers**: Staff can see different information about customers of their airline.
    1. `staffTopCustomer()`: shows the most frequent customer within the last year.
    2. `staffCustomerFlight()`: shows a list of flights in their airline that this customer has taken.
    3. `staffFlightCustomer()`: shows a list of customers of this flight in their airline.
```
# most frequent customer
query1 = """
        SELECT email, name, COUNT(ticket_id) AS ticket \
        FROM customer, purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
        WHERE email = customer_email AND username = \'{}\' AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 365 \
        GROUP BY email, name \
        ORDER BY ticket \
        DESC LIMIT 1
        """

# a list of flights a customer took
query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
query2 = """
    SELECT DISTINCT airplane_id, flight_num, departure_airport, arrival_airport, \
        departure_time, arrival_time, status \
    FROM customer, purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
        WHERE email = \'{}\' and email = customer_email and username = \'{}\'"""
query1 = """
    SELECT email, name, COUNT(ticket_id) AS ticket \
    FROM customer, purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
    WHERE email = customer_email AND username = \'{}\' \
        AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 365\
    GROUP BY email, name \
    ORDER BY ticket \
    DESC LIMIT 1
    """

# a list of customers who took a flight
query = "SELECT username, airline_name FROM airlineStaff WHERE username = \'{}\'"
query3 = """
        SELECT DISTINCT email, name 
        FROM customer, purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff\
        WHERE flight_num = \'{}\' and email = customer_email and username = \'{}\'
        """
query1 = """
        SELECT email, name, COUNT(ticket_id) AS ticket 
        FROM customer, purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
        WHERE email = customer_email AND username = \'{}\' and DATEDIFF(CURDATE(), DATE(purchase_date)) < 365\
        GROUP BY email, name\
        ORDER BY ticket DESC 
        LIMIT 1
        """
```

5. **numbers**: Staff can see relevant numbers that help them understand the business of their airline.
    1. `staffTicketReport()`: renders the ticket front page.
    2. `staffTicket()`: shows the total amounts of ticket sold and monthly tickets sold breakdown in a bar chart from on a selected period.
    3. `staffEarningsReport()`: shows pie charts of total revenue earned from direct sales (customer directly buying from airline) and indirect sales (customers buying through agent) in the past month and past year.
    4. `staffTopDestinations()`: shows the top 3 most popular destination for the past 3 months and past year.
```
# tickets
ticket = """
        SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, count(ticket_id) FROM \
        purchase NATURAL JOIN airlineStaff NATURAL JOIN flight NATURAL JOIN ticket\
        WHERE purchase_date > \'{}\'\
        and purchase_date < \'{}\' AND username = \'{}\' \
        GROUP BY year, month\
        ORDER BY year, month
        """

        
# earnings
query3 = """
        SELECT SUM(price)\
        FROM purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
        WHERE username = \'{}\' AND booking_agent_id IS NULL \
            AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 30 \
        GROUP BY airline_name
        """
query4 = """
        SELECT SUM(price)\
        FROM purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
        WHERE username = \'{}\' AND booking_agent_id IS NOT NULL \
            AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 30 \
        GROUP BY airline_name
        """
query5 = """
        SELECT SUM(price) \
        FROM purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
        WHERE username = \'{}\' AND booking_agent_id IS NULL \
            AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 365\
        GROUP BY airline_name
        """
query6 = """
        SELECT SUM(price)\
        FROM purchase NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airlineStaff \
        WHERE username = \'{}\' AND booking_agent_id IS NOT NULL \
            AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 365 \
        GROUP BY airline_name
        """

# top destinations
query1 = """
        SELECT airport_city, count(ticket_id) AS ticket \
        FROM purchase NATURAL JOIN ticket NATURAL JOIN flight, airport \
        WHERE airport_name = arrival_airport AND \
            DATEDIFF(CURDATE(), DATE(purchase_date)) < 90 \
        GROUP BY airport_city \
        ORDER BY ticket DESC \
        LIMIT 3
        """

query2 = """
        SELECT airport_city, COUNT(ticket_id) AS ticket \
        FROM purchase NATURAL JOIN ticket NATURAL JOIN flight, airport \
        WHERE airport_name = arrival_airport \
            AND DATEDIFF(CURDATE(), DATE(purchase_date)) < 365\
        GROUP BY airport_city \
        ORDER BY ticket DESC \
        LIMIT 3
        """
```