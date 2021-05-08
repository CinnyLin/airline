CREATE VIEW customer_spending AS 
SELECT *
FROM purchase NATURAL JOIN ticket NATURAL JOIN flight;

CREATE VIEW agent_commission AS 
SELECT email, purchase.ticket_id, customer_email, purchase_date, price AS ticket_price
FROM bookingAgent NATURAL JOIN purchase NATURAL JOIN ticket NATURAL JOIN flight;

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
