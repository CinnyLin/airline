-- --------------------------------------------------------
-- Cinny added ON DELETE CASCADE to all foreign keys for delete account function


-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `airline_name` varchar(50) NOT NULL,
  PRIMARY KEY(`airline_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `airlineStaff`
--

CREATE TABLE `airlineStaff` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  PRIMARY KEY(`username`),
  FOREIGN KEY(`airline_name`) REFERENCES `airline`(`airline_name`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `airline_name` varchar(50) NOT NULL,
  `airplane_id` int(11) NOT NULL,
  `seats` int(11) NOT NULL,
  PRIMARY KEY(`airline_name`, `airplane_id`),
  FOREIGN KEY(`airline_name`) REFERENCES `airline`(`airline_name`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `airport_name` varchar(50) NOT NULL,
  `airport_city` varchar(50) NOT NULL,
  PRIMARY KEY(`airport_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `bookingAgent`
--

CREATE TABLE `bookingAgent` (
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `booking_agent_id` int(11) NOT NULL,
  PRIMARY KEY(`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `email` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `building_number` varchar(30) NOT NULL,
  `street` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `state` varchar(30) NOT NULL,
  `phone_number` int(11) NOT NULL,
  `passport_number` varchar(30) NOT NULL,
  `passport_expiration` date NOT NULL,
  `passport_country` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  PRIMARY KEY(`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `airline_name` varchar(50) NOT NULL,
  `flight_num` int(11) NOT NULL,
  `departure_airport` varchar(50) NOT NULL,
  `departure_time` datetime NOT NULL,
  `arrival_airport` varchar(50) NOT NULL,
  `arrival_time` datetime NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `status` varchar(50) NOT NULL,
  `airplane_id` int(11) NOT NULL,
  `num_tickets_left` int(11), -- Cinny added
  PRIMARY KEY(`airline_name`, `flight_num`),
  FOREIGN KEY(`airline_name`, `airplane_id`) REFERENCES `airplane`(`airline_name`, `airplane_id`) ON DELETE CASCADE,
  FOREIGN KEY(`departure_airport`) REFERENCES `airport`(`airport_name`) ON DELETE CASCADE,
  FOREIGN KEY(`arrival_airport`) REFERENCES `airport`(`airport_name`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `ticket_id` int(11) NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  `flight_num` int(11) NOT NULL,
  PRIMARY KEY(`ticket_id`),
  FOREIGN KEY(`airline_name`, `flight_num`) REFERENCES `flight`(`airline_name`, `flight_num`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Table structure for table `purchase`
--

CREATE TABLE `purchase` (
  `ticket_id` int(11) NOT NULL,
  `customer_email` varchar(50) NOT NULL,
  `booking_agent_id` int(11),
  `booking_agent_email` varchar(50), -- Cinny added
  `purchase_date` date NOT NULL,
  PRIMARY KEY(`ticket_id`, `customer_email`),
  FOREIGN KEY(`ticket_id`) REFERENCES `ticket`(`ticket_id`) ON DELETE CASCADE,
  FOREIGN KEY(`customer_email`) REFERENCES `customer`(`email`) ON DELETE CASCADE,
  FOREIGN KEY(`booking_agent_email`) REFERENCES `bookingAgent`(`email`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;