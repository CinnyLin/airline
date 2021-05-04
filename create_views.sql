CREATE VIEW customer_spending AS 
SELECT *
FROM purchase NATURAL JOIN ticket NATURAL JOIN flight;

CREATE VIEW agent_commission AS 
SELECT email, purchase.ticket_id, customer_email, purchase_date, price AS ticket_price
FROM bookingAgent NATURAL JOIN purchase NATURAL JOIN ticket NATURAL JOIN flight;
