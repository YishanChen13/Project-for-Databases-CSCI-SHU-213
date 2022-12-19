#a
INSERT INTO airline (airline_name) VALUES 
('China Eastern'),
('Delta'),
('United');

#b
INSERT INTO airport (airport_name, city) VALUES 
('JFK', 'New York City'),
('PVG', 'Shanghai'),
('PEK', 'Beijing');

#c
INSERT INTO customer (customer_email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth) VALUES
('bob@nyu.edu', 'Bob', md5('bob1234'), 'B1', 'Banana Street', 'New York City', 'NY', '1234-1234-1234', '111222333', '2022-12-18', 'USA', '2000-01-01'),
('rob@nyu.edu', 'Rob', md5('rob1234'), 'B1', 'Banana Street', 'New York City', 'NY', '1233-1233-1233', '111222444', '2024-12-12', 'USA', '2000-01-01'),
('tom@nyu.edu', 'Tom', md5('tom1234'), 'T1', 'Tomato Street', 'Chicago', 'IL', '4321-4321-4321', '333222111', '2022-11-11', 'USA', '2001-01-01');

#d
INSERT INTO booking_agent (booking_agent_email, booking_agent_ID, password) VALUES
("sam@nyu.edu", 3333, md5("sam1234")),
("jess@nyu.edu", 4444, md5("jess1234"));

#e
INSERT INTO airplane (airplane_ID, airline_name, num_of_seats) VALUES
(1234, 'China Eastern', 3),
(2345, 'Delta', 3),
(3456, 'United', 3);

#f
INSERT INTO airline_staff (username, airline_name, password, first_name, last_name, date_of_birth, admin, operator) VALUES
('ian@nyu.edu', 'China Eastern', md5("ian1234"), 'Ian', 'Chen', '1990-09-09', false, false),
('jack@nyu.edu', 'China Eastern', md5("jack1234"), 'Jack', 'Chen', '1990-09-09', true, true);

#g
INSERT INTO flight (flight_num, airline_name, airplane_ID, departure_airport, arrival_airport, departure_time, arrival_time, price, status) VALUES
(9999, 'China Eastern', 1234, 'JFK', 'PVG', '2022-12-25 01:00:00', '2022-12-25 20:00:00', 1000, 'upcoming'),
(8888, 'China Eastern', 1234, 'PVG', 'JFK', '2022-12-26 01:00:00', '2022-12-26 20:00:00', 1000, 'upcoming'),
(7777, 'Delta', 2345, 'JFK', 'PVG', '2022-12-25 01:00:00', '2022-12-25 20:00:00', 1000, 'upcoming'),
(6666, 'Delta', 2345, 'PVG', 'JFK', '2022-12-26 01:00:00', '2022-12-26 20:00:00', 1000, 'upcoming'),
(5555, 'United', 3456, 'JFK', 'PVG', '2021-10-15 01:00:00', '2021-10-15 20:00:00', 1000, 'finished'),
(4444, 'United', 3456, 'PVG', 'PEK', '2021-10-16 01:00:00', '2021-10-16 20:00:00', 1000, 'finished');

#h
INSERT INTO ticket (ticket_id, airline_name, flight_num) VALUES
(111, 'China Eastern', 9999),
(112, 'China Eastern', 9999),
(113, 'China Eastern', 9999),
(222, 'China Eastern', 8888),
(223, 'China Eastern', 8888),
(333, 'United', 5555),
(334, 'United', 5555);

#i
INSERT INTO purchases (ticket_id, customer_email, booking_agent_ID, purchase_date) VALUES
(111, 'tom@nyu.edu', 3333, '2022-12-15'),
(112, 'bob@nyu.edu', null, '2022-10-15'),
(113, 'rob@nyu.edu', null, '2022-10-15'),
(222, 'tom@nyu.edu', 3333, '2022-11-15'),
(223, 'bob@nyu.edu', 4444, '2022-12-15'),
(333, 'bob@nyu.edu', 3333, '2021-01-15'),
(334, 'tom@nyu.edu', null, '2021-01-15');

#j
INSERT INTO works_with (booking_agent_email, airline_name) VALUES
('sam@nyu.edu', 'China Eastern'),
('jess@nyu.edu', 'China Eastern');