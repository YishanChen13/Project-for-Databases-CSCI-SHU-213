CREATE TABLE airline (
    airline_name VARCHAR(50) NOT NULL,
    PRIMARY KEY(airline_name)
);

CREATE TABLE airline_staff (
    username VARCHAR(50) NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    password VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    admin BOOLEAN NOT NULL,
    operator BOOLEAN NOT NULL,
    PRIMARY KEY(username),
    FOREIGN KEY (airline_name) REFERENCES airline(airline_name)
);

CREATE TABLE airplane (
    airplane_ID INT(10) NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    num_of_seats INT(10),
    PRIMARY KEY(airplane_ID, airline_name),
    FOREIGN KEY(airline_name) REFERENCES airline(airline_name)
);

CREATE TABLE airport (
    airport_name VARCHAR(50) NOT NULL,
    city VARCHAR(50),
    PRIMARY KEY(airport_name)
);

CREATE TABLE flight (
    flight_num INT(10) NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    airplane_ID INT(10) NOT NULL,
    departure_airport VARCHAR(50) NOT NULL,
    arrival_airport VARCHAR(50) NOT NULL,
    departure_time DATETIME,
    arrival_time DATETIME,
    price DECIMAL(10,0),
    status VARCHAR(50),
    PRIMARY KEY(flight_num, airline_name),
    FOREIGN KEY(airline_name, airplane_ID) REFERENCES airplane(airline_name, airplane_ID),
    FOREIGN KEY(departure_airport) REFERENCES airport(airport_name),
    FOREIGN KEY(arrival_airport) REFERENCES airport(airport_name)
);


CREATE TABLE ticket (
    ticket_id INT(10) NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    flight_num INT(10) NOT NULL,
    PRIMARY KEY(ticket_id),
    FOREIGN KEY(airline_name) REFERENCES flight(airline_name),
    FOREIGN KEY(flight_num) REFERENCES flight(flight_num)
);

CREATE TABLE booking_agent (
    booking_agent_email VARCHAR(50) NOT NULL,
    booking_agent_ID INT(10) UNIQUE,
    password VARCHAR(50),
    PRIMARY KEY(booking_agent_email) 
);

CREATE TABLE customer (
    customer_email VARCHAR(50) NOT NULL,
    name VARCHAR(50),
    password VARCHAR(50),
    building_number VARCHAR(50),
    street VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    phone_number VARCHAR(50),
    passport_number VARCHAR(50),
    passport_expiration DATE,
    passport_country VARCHAR(50),
    date_of_birth DATE,
    PRIMARY KEY(customer_email)
);

CREATE TABLE purchases (
    ticket_id INT(10) NOT NULL,
    customer_email VARCHAR(50) NOT NULL,
    booking_agent_ID INT(10),
    purchase_date DATE,
    PRIMARY KEY(ticket_id, customer_email),
    FOREIGN KEY(ticket_id) REFERENCES ticket(ticket_id),
    FOREIGN KEY(customer_email) REFERENCES customer(customer_email),
    FOREIGN KEY(booking_agent_ID) REFERENCES booking_agent(booking_agent_ID)
);

CREATE TABLE works_with (
    booking_agent_email VARCHAR(50) NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    PRIMARY KEY(booking_agent_email, airline_name),
    FOREIGN KEY(booking_agent_email) REFERENCES booking_agent(booking_agent_email),
    FOREIGN KEY(airline_name) REFERENCES airline(airline_name)
);