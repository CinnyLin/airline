-- --------------------------------------------------------
-- except from airline data everything else can be added from front-end

-- --------------------------------------------------------

--
-- Data for table `airline` (airline_name)
--

INSERT INTO airline VALUES
("Air Arabia"), ("Air China"), ("Air France"), ("American Airlines"), 
("Cathay Pacific"), ("China Airlines"), ("China Eastern"), ("China Southern"), 
("British Airways"), ("Delta"), ("EVA Air"), ("Lufthansa");

-- --------------------------------------------------------

--
-- Data for table `airlineStaff`
-- (username, password, first_name, last_name, date_of_birth, airline_name)
--

INSERT INTO airlineStaff VALUES
-- ("staff@gmail.com", "password123", "Cinny", "Lin", "1999-12-31", "EVA Air"), -- front-end test
-- md5(password123) = 9df7a7314e3884b26222e2ccd834aa24
("airstaff123", "9df7a7314e3884b26222e2ccd834aa24", "Zoe", "Xiao", "2000-05-16", "China Eastern");

-- --------------------------------------------------------

--
-- Data for table `airplane`
-- (airline_name, airplane_id, seats)
--

INSERT INTO airplane VALUES
-- ("Air China", 1, 100), -- front-end test
("Air Arabia", 100, 50),
("Air Arabia", 120, 100),
("Air Arabia", 121, 100),
("Air Arabia", 130, 100),
("Air Arabia", 131, 100),
("Air Arabia", 150, 100),

("Air France", 100, 100),
("Air France", 130, 100),
("Air France", 131, 100),
("Air France", 132, 80),
("Air France", 150, 150),
("British Airways", 100, 100), 
("British Airways", 101, 100), 
("British Airways", 102, 100), 
("British Airways", 130, 80), 
("British Airways", 150, 80), 
("Lufthansa", 100, 100),
("Lufthansa", 130, 120),
("Lufthansa", 131, 120),
("Lufthansa", 120, 120),
("Lufthansa", 150, 120),

("American Airlines", 100, 100), 
("American Airlines", 150, 120), 
("American Airlines", 101, 100), 
("American Airlines", 120, 100), 
("American Airlines", 130, 100), 
("American Airlines", 131, 100), 
("American Airlines", 132, 100), 
("American Airlines", 151, 120),  
("Delta", 120, 80),
("Delta", 130, 100),
("Delta", 150, 100),
("Delta", 140, 100),
("Delta", 141, 100),
("Delta", 151, 100),
("Delta", 152, 100),
("Delta", 142, 100),


("Air China", 120, 100),
("Air China", 100, 80),
("Air China", 130, 100),

("Cathay Pacific", 100, 80),
("Cathay Pacific", 120, 100),
("Cathay Pacific", 101, 80),

("China Airlines", 130, 100), 
("China Airlines", 120, 100), 
("China Airlines", 121, 100), 

("China Eastern", 120, 100), 
("China Eastern", 130, 100), 
("China Eastern", 131, 100), 

("China Southern", 100, 80), 
("China Southern", 101, 80), 
("China Southern", 102, 80), 

("EVA Air", 130, 100),
("EVA Air", 120, 100),
("EVA Air", 100, 80);
-- --------------------------------------------------------

--
-- Data for table `airport`
-- (airport_name, airport_city)
--

INSERT INTO airport VALUES
("JFK", "New York"), ("PVG", "Shanghai"), -- front-end test
("CMN", "Cascablanca"), ("AUH", "Abu Dhabi"), -- Air Arabia
("PEK", "Beijing"), ("CAN", "Guangzhou"), ("SHA", "Shanghai"), -- Air China, China Airlines, China Eastern, China Southern
("LHR", "London"), ("AMS", "Amsterdam"), ("CDG", "Paris"), 
("FRA", "Frankfurt"), ("MAD", "Madrid"), -- Air France, British Airways, Lufthansa
("LAX", "Los Angeles"), ("ATL", "Atlanta"), ("DFW", "Dallas"),
("SFO", "San Francisco"), ("ORD", "Chicago"), ("SEA", "Seattle"),
("MIA", "Miami"), ("DTW", "Detriot"), -- American Airlines, Delta
("HKG", "Hong Kong"), -- Cathay Pacific
("TPE", "Taoyuan"), ("TSA", "Taipei"); -- Eva Air

-- --------------------------------------------------------

--
-- Data for table `bookingAgent`
-- (email, password, booking_agent_id)
--

INSERT INTO bookingAgent VALUES
-- ("agent@gmail.com", "password123", 1), -- front-end test
("agent2@gmail.com", "9df7a7314e3884b26222e2ccd834aa24", 2);


-- --------------------------------------------------------

--
-- Data for table `customer`
-- (email, name, password, 
-- building_number, street, city, state, phone_number,
-- passport_number, passport_expiration, passport_country
-- date_of_birth)
--

INSERT INTO customer VALUES
-- ("customer@nyu.edu", "Cinny", "password123", 1555, "Century Avenue", "Shanghai", "China", 1234567890, 1234567890, "2022-05-30", "Taiwan", "1999-12-31"),
("customer2@nyu.edu", "Zoe", "9df7a7314e3884b26222e2ccd834aa24", 1555, "Century Avenue", "Shanghai", "China", 1234567890, 1234567890, "2022-05-30", "China", "2000-05-17");

-- --------------------------------------------------------

--
-- Data for table `flight`
-- (airline_name, flight_num, 
-- departure_airport, departure_time, arrival_airport, arrival_time, 
-- price, status, airplane_id, num_tickets_left)
--

INSERT INTO flight VALUES
-- Middle Eastern Airlines/Airports
("Air Arabia", 10100, "CMN", "2021-05-30 15:20", "AUH", "2021-05-30 17:20", 500, "in-progress", 100, 50),
("Air Arabia", 10120, "CMN", "2021-05-30 15:20", "FRA", "2021-05-31 18:20", 1000, "upcoming", 120, 100),
("Air Arabia", 10121, "CMN", "2021-05-30 15:20", "LHR", "2021-05-31 18:20", 1000, "upcoming", 121, 100),
("Air Arabia", 10130, "AUH", "2021-05-30 15:20", "LAX", "2021-05-31 20:20", 1000, "in-progress", 130, 100),
("Air Arabia", 10131, "AUH", "2021-05-30 15:20", "DTW", "2021-05-31 20:20", 1000, "upcoming", 131, 100),
("Air Arabia", 10150, "AUH", "2021-05-30 15:20", "HKG", "2021-05-31 23:20", 1500, "delayed", 150, 100),

-- European Airlines/Airports
("Air France", 20100, "CDG", "2021-05-30 15:20", "LHR", "2021-05-30 17:20", 500, "in-progress", 100, 100),
("Air France", 20130, "CDG", "2021-05-30 15:20", "ATL", "2021-05-30 21:20", 1000, "delayed", 130, 100),
("Air France", 20131, "CDG", "2021-05-30 15:20", "SFO", "2021-05-30 20:20", 1200, "upcoming", 131, 100),
("Air France", 20132, "CDG", "2021-05-30 15:20", "MIA", "2021-05-31 20:20", 1000, "upcoming", 132, 80),
("Air France", 20150, "CDG", "2021-05-30 15:20", "TPE", "2021-05-31 15:20", 1500, "upcoming", 150, 150),

("British Airways", 21100, "LHR", "2021-05-30 15:20", "AMS", "2021-05-30 17:20", 500, "in-progress", 100, 100),
("British Airways", 21101, "LHR", "2021-05-30 15:20", "FRA", "2021-05-30 17:20", 500, "delayed", 101, 100),
("British Airways", 21102, "LHR", "2021-05-30 15:20", "MAD", "2021-05-30 17:20", 500, "delayed", 102, 100),
("British Airways", 21130, "LHR", "2021-05-30 15:20", "DFW", "2021-05-31 20:20", 1000, "upcoming", 130, 80),
("British Airways", 21150, "LHR", "2021-05-30 15:20", "HKG", "2021-05-31 15:20", 1500, "upcoming", 150, 80),

("Lufthansa", 22100, "FRA", "2021-05-30 15:20", "LHR", "2021-05-30 18:20", 500, "in-progress", 100, 100),
("Lufthansa", 22130, "FRA", "2021-05-30 15:20", "ORD", "2021-05-30 20:20", 1000, "in-progress", 130, 120),
("Lufthansa", 22131, "FRA", "2021-05-30 15:20", "SEA", "2021-05-30 20:20", 1000, "delayed", 131, 120),
("Lufthansa", 22120, "FRA", "2021-05-30 15:20", "AUH", "2021-05-30 18:20", 800, "upcoming", 120, 120),
("Lufthansa", 22150, "FRA", "2021-05-30 15:20", "PEK", "2021-05-31 18:20", 1500, "upcoming", 150, 120),


-- American Airlines/Airports
("American Airlines", 30100, "LAX", "2021-05-30 15:20", "JFK", "2021-05-30 19:20", 500, "in-progress", 100, 100),
("American Airlines", 30150, "LAX", "2021-05-30 15:20", "PVG", "2021-05-31 17:20", 1500, "delayed", 150, 120),
("American Airlines", 30101, "ATL", "2021-05-30 15:20", "JFK", "2021-05-30 18:20", 500, "delayed", 101, 100),
("American Airlines", 30120, "ATL", "2021-05-30 15:20", "CMN", "2021-05-30 21:20", 800, "delayed", 120, 100),
("American Airlines", 30130, "DFW", "2021-05-30 15:20", "FRA", "2021-05-31 21:20", 1000, "delayed", 130, 100),
("American Airlines", 30131, "DFW", "2021-05-30 15:20", "LHR", "2021-05-31 18:20", 1000, "upcoming", 131, 100),
("American Airlines", 30132, "DTW", "2021-05-30 15:20", "AMS", "2021-05-30 18:20", 1000, "upcoming", 132, 100),
("American Airlines", 30151, "DTW", "2021-05-30 15:20", "TPE", "2021-05-31 19:20", 1500, "upcoming", 151, 120),

("Delta", 31120, "SFO", "2021-05-30 15:20", "CAN", "2021-05-31 18:20", 800, "in-progress", 120, 80),
("Delta", 31130, "SFO", "2021-05-30 15:20", "CDG", "2021-05-31 18:20", 1000, "delayed", 130, 100),
("Delta", 31150, "ORD", "2021-05-30 15:20", "SHA", "2021-05-31 18:20", 1500, "delayed", 150, 100),
("Delta", 31140, "ORD", "2021-05-30 15:20", "SFO", "2021-05-31 18:20", 1000, "upcoming", 140, 100),
("Delta", 31141, "SEA", "2021-05-30 15:20", "MIA", "2021-05-31 18:20", 1000, "upcoming", 141, 100),
("Delta", 31151, "SEA", "2021-05-30 15:20", "HKG", "2021-05-31 18:20", 1500, "upcoming", 151, 100),
("Delta", 31152, "MIA", "2021-05-30 15:20", "TSA", "2021-05-31 18:20", 1500, "upcoming", 152, 100),
("Delta", 31142, "MIA", "2021-05-30 15:20", "DTW", "2021-05-31 18:20", 1000, "upcoming", 142, 100),

-- Chinese Airlines/Airports
("Air China", 52120, "PEK", "2021-05-30 15:20", "JFK", "2021-05-31 18:20", 1500, "in-progress", 120, 100),
("Air China", 52100, "PEK", "2021-05-30 15:20", "PVG", "2021-05-31 18:20", 500, "delayed", 100, 80),
("Air China", 52130, "PVG", "2021-05-30 15:20", "AUH", "2021-05-31 18:20", 1200, "upcoming", 130, 100),

("Cathay Pacific", 51100, "HKG", "2021-05-30 15:20", "TSA", "2021-05-31 18:20", 500, "in-progress", 100, 80),
("Cathay Pacific", 51120, "HKG", "2021-05-30 15:20", "LHR", "2021-05-31 18:20", 1000, "upcoming", 120, 100),
("Cathay Pacific", 51101, "HKG", "2021-05-30 15:20", "SHA", "2021-05-31 18:20", 500, "upcoming", 101, 80),

("China Airlines", 53130, "PEK", "2021-05-30 15:20", "CAN", "2021-05-31 18:20", 500, "delayed", 130, 100),
("China Airlines", 53120, "PVG", "2021-05-30 15:20", "LHR", "2021-05-31 18:20", 500, "delayed", 120, 100),
("China Airlines", 53121, "SHA", "2021-05-30 15:20", "AMS", "2021-05-31 18:20", 500, "upcoming", 121, 100),

("China Eastern", 54120, "PVG", "2021-05-30 15:20", "CDG", "2021-05-31 18:20", 500, "in-progress", 120, 100),
("China Eastern", 54130, "PVG", "2021-03-29 14:40", "LAX", "2021-03-29 17:40", 500, "delayed", 130, 100),
("China Eastern", 54131, "SHA", "2021-12-30 21:30", "DTW", "2021-12-31 03:30", 500, "upcoming", 131, 100),

("China Southern", 55100, "CAN", "2021-05-30 15:20", "HKG", "2021-05-31 18:20", 500, "in-progress", 100, 80),
("China Southern", 55101, "CAN", "2021-05-30 15:20", "TPE", "2021-05-31 18:20", 500, "upcoming", 101, 80),
("China Southern", 55102, "CAN", "2021-05-30 15:20", "TSA", "2021-05-31 18:20", 500, "upcoming", 102, 80),

("EVA Air", 50130, "TPE", "2021-05-30 15:20", "JFK", "2021-05-31 18:20", 1000, "in-progress", 130, 100),
("EVA Air", 50120, "TPE", "2021-05-30 15:20", "FRA", "2021-05-31 18:20", 1200, "delayed", 120, 100),
("EVA Air", 50100, "TSA", "2021-05-30 15:20", "PVG", "2021-05-31 18:20", 500, "upcoming", 100, 80);

-- --------------------------------------------------------

--
-- Data for table `ticket`
-- (ticket_id, airline_name, flight_num)
--

INSERT INTO ticket VALUES
(1, "EVA Air", 50100), -- front-end test
(2, "China Eastern", 54120);

-- --------------------------------------------------------

--
-- Data for table `purchase`
-- (ticket_id, customer_email, booking_agent_id, booking_agent_email, purchase_date)
--

-- INSERT INTO purchase VALUES 
-- (1, "customer@nyu.edu", 1, "agent@gmail.com","2021-04-30"); -- front-end test
INSERT INTO purchase (ticket_id, customer_email, purchase_date) VALUES 
(2, "customer2@nyu.edu", "2021-04-19");
