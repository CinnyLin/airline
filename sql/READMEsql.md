# `sql`

## `create_tables.sql`
create basic table structures *
1. **airline**: airline, airplane, airport, flight
2. **people**: airlineStaff, bookingAgent, customer
3. **relations**: ticket, purchase

**Additional Notes*
1. added `ON DELETE CASCADE` for all foreign key functions to support `deleteAccount` and `resetPassword` functions
```
# e.g. airlineStaff table

CREATE TABLE `airlineStaff` (
  ...
  PRIMARY KEY(`username`),
  FOREIGN KEY(`airline_name`) REFERENCES `airline`(`airline_name`) ON DELETE CASCADE
);
```

2. added `num_tickets` in flight table and wrote python logic for the front-end to check if the number of tickets left in `flight` matches the number of seats in `airplane`
```
# flight table
CREATE TABLE `flight` (
  ...
  `num_tickets_left` int(11), -- Cinny added
  PRIMARY KEY(`airline_name`, `flight_num`),
  FOREIGN KEY(`airline_name`, `airplane_id`) REFERENCES `airplane`(`airline_name`, `airplane_id`) ON DELETE CASCADE,
  ...
);

# airplane table
CREATE TABLE `airplane` (
  ...
  `seats` int(11) NOT NULL,
  PRIMARY KEY(`airline_name`, `airplane_id`),
  FOREIGN KEY(`airline_name`) REFERENCES `airline`(`airline_name`) ON DELETE CASCADE
);

# pyhton logic
num = "SELECT seats FROM airplane NATURAL JOIN airlineStaff WHERE username = \'{}\' and airplane_id = \'{}\'"
cursor.execute(num.format(username, airplane_id))
num = cursor.fetchone()
if int(seats) >= int(num[0]):
    num_error = "The number of seats left cannot be more than the airplane seats."
```

## `create_triggers.sql`
1. created a trigger `delete_tickets` that updates num_tickets when customer or agent make purchase so that buyer can be informed when there is no tickets left for the flight they are interested in
```
DROP trigger IF EXISTS delete_tickets;
CREATE trigger delete_tickets AFTER INSERT ON purchase
for each ROW 
	UPDATE flight NATURAL JOIN ticket NATURAL JOIN purchase
    SET num_tickets_left = num_tickets_left - 1
    WHERE NEW.ticket_id = ticket.ticket_id;
```

## `create_views.sql`
created three views to support easier queries in python functions
1. `customer_spending` view supports `customerTrackSpending()` function, graphs monthly customer spending in a selected period of time
```
CREATE VIEW customer_spending AS 
SELECT *
FROM purchase NATURAL JOIN ticket NATURAL JOIN flight;
```

2. `agent_commission` view supports `agentCommission()` function, graphs monthly commission an agent receives in a selected period of time.
```
CREATE VIEW agent_commission AS 
SELECT email, purchase.ticket_id, customer_email, purchase_date, price AS ticket_price
FROM bookingAgent NATURAL JOIN purchase NATURAL JOIN ticket NATURAL JOIN flight;
```

3. `agent_view_flight` view supports `agentViewTicket()` function, renders a table showing the agent the upcoming flights they booked for their customers
```
CREATE VIEW agent_view_flight AS
SELECT bookingAgent.email, purchase.booking_agent_id, 
    purchase.customer_email, purchase.purchase_date, purchase.ticket_id, 
    flight.airline_name, flight.flight_num, 
    Depart.airport_city as departure_city, departure_airport, departure_time, 
    Arrive.airport_city as arrival_city, arrival_airport, arrival_time, 
    price, status, airplane_id
FROM bookingAgent NATURAL RIGHT OUTER JOIN purchase NATURAL JOIN ticket 
    NATURAL JOIN flight, airport AS Depart, airport AS Arrive
WHERE Depart.airport_name = departure_airport and Arrive.airport_name = arrival_airport;
```

## `insert_data.sql`: insert test data
created a great amount of synthesized data for testing, including 12 airlines, 50 airplanes, 23 airports, and over 100 flights.