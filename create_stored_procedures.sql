-- define trigger which updates num_tickets_left

-- deletes tickets when customer or agent make purchase
DROP trigger IF EXISTS delete_tickets;
CREATE trigger delete_tickets AFTER INSERT ON purchase
for each ROW 
	UPDATE flight NATURAL JOIN ticket NATURAL JOIN purchase
    SET num_tickets_left = num_tickets_left - 1
    WHERE NEW.ticket_id = ticket.ticket_id;


-- check all your triggers
show triggers;
