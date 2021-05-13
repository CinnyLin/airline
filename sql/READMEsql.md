# `sql`

## `create_tables.sql`
create basic table structures *
1. **airline**: airline, airplane, airport, flight
2. **people**: airlineStaff, bookingAgent, customer
3. **relations**: ticket, purchase

**Additional Notes*
1. added `ON DELETE CASCADE` for all foreign key functions to support `deleteAccount` and `resetPassword` functions
2. added `num_tickets` in flight table and wrote python logic for the front-end to check if the number of tickets left in `flight` matches the number of seats in `airplane`

## `create_triggers.sql`
1. created a trigger `delete_tickets` that updates num_tickets when customer or agent make purchase so that buyer can be informed when there is no tickets left for the flight they are interested in
<!-- ```
DROP trigger IF EXISTS delete_tickets;
CREATE trigger delete_tickets AFTER INSERT ON purchase
for each ROW 
	UPDATE flight NATURAL JOIN ticket NATURAL JOIN purchase
    SET num_tickets_left = num_tickets_left - 1
    WHERE NEW.ticket_id = ticket.ticket_id;
``` -->

## `create_views.sql`
created three views to support easier queries in python functions
1. `customer_spending` view supports `customerTrackSpending()` function, graphs monthly customer spending in a selected period of time
2. `agent_commission` view supports `agentCommission()` function, graphs monthly commission an agent receives in a selected period of time
3. `agent_view_flight` view supports `agentViewTicket()` function, renders a table showing the agent the upcoming flights they booked for their customers

## `insert_data.sql`: insert test data
created a great amount of synthesized data for testing, including 12 airlines, 50 airplanes, 23 airports, and over 100 flights.