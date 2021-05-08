-- define trigger which updates num_tickets_left

DROP trigger IF EXISTS add_tickets;
CREATE trigger add_tickets BEFORE INSERT ON ticket
for each ROW
	UPDATE flight
    SET num_tickets_left = num_tickets_left + 1
    WHERE flight.airline_name = NEW.airline_name and flight.flight_num = NEW.flight_num;

DROP trigger IF EXISTS delete_tickets;
CREATE trigger delete_tickets AFTER INSERT ON purchase
for each ROW 
	UPDATE flight NATURAL JOIN ticket NATURAL JOIN purchase
    SET num_tickets_left = num_tickets_left - 1
    WHERE NEW.ticket_id = ticket.ticket_id;


-- check all your triggers
show triggers;
