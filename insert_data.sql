-- --------------------------------------------------------

--
-- Data for table `airline` (airline_name)
--

INSERT INTO airline 
VALUES ("China Eastern");

-- --------------------------------------------------------

--
-- Data for table `airlineStaff`
-- (username, password, first_name, last_name, date_of_birth, airline_name)
--

INSERT INTO airlineStaff
VALUES ("airstaff123", "password123", "Zoe", "Xiao", "2000-05-17", "China Eastern");

-- --------------------------------------------------------

--
-- Data for table `airplane`
-- (airline_name, airplane_id, seats)
--

INSERT INTO airplane 
VALUES ("China Eastern", 123, 100), ("China Eastern", 125, 80), ("China Eastern", 127, 120);

-- --------------------------------------------------------

--
-- Data for table `airport`
-- (airport_name, airport_city)
--

INSERT INTO airport
VALUES ("JFK", "NYC"), ("PVG", "Shanghai");

-- --------------------------------------------------------

--
-- Data for table `bookingAgent`
-- (email, password, booking_agent_id)
--

INSERT INTO bookingAgent 
VALUES ("booking@gmail.com", "password123", 100);

-- --------------------------------------------------------

--
-- Data for table `customer`
-- (email, name, password, 
-- building_number, street, city, state, phone_number,
-- passport_number, passport_expiration, passport_country
-- date_of_birth)
--

INSERT INTO customer VALUES
("ycl461@nyu.edu", "Cinny", "password123", 30, "Cherry Blossom Street", "Taipei", "Taiwan", 1432563, 5246351, "2022-05-25", "Taiwan", "1999-12-31");

-- --------------------------------------------------------

--
-- Data for table `flight`
-- (airline_name, flight_num, 
-- departure_airport, departure_time, arrival_airport, arrival_time, 
-- price, status, airplane_id)
--

INSERT INTO flight VALUES
("China Eastern", 34123, "PVG", "2021-03-30 15:20", "JFK", "2021-03-30 18:20", 500, "in-progress", 123),
("China Eastern", 34125, "PVG", "2021-03-29 14:40", "JFK", "2021-03-29 17:40", 500, "delayed", 125),
("China Eastern", 34127, "JFK", "2021-12-30 21:30", "PVG", "2021-12-31 03:30", 500, "upcoming", 127);

-- --------------------------------------------------------

--
-- Data for table `ticket`
-- (ticket_id, airline_name, flight_num)
--

INSERT INTO ticket 
VALUES (1, "China Eastern", 34123), (2, "China Eastern", 34123), (3, "China Eastern", 34125), (4, "China Eastern", 34127);

INSERT INTO purchase
VALUES (1, "ycl461@nyu.edu", 100, "2021-03-30");
