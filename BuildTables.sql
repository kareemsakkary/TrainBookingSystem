CREATE TABLE Account
(
 account_id INT NOT NULL IDENTITY(1,1),
 email VARCHAR(255) NOT NULL,
 password VARCHAR(255) NOT NULL,
 role VARCHAR(255) NOT NULL,
 name VARCHAR(255) NOT NULL,
 phone_num VARCHAR(255) NOT NULL,
 address VARCHAR(255) NOT NULL,
 date_of_birth DATE NOT NULL,
 PRIMARY KEY (account_id),

 -- Check that the role is one of "admin" or "customer"
 CHECK (role IN ('admin', 'customer'))
);


CREATE TABLE Train
(
 train_id INT NOT NULL IDENTITY(1,1),
 capacity INT NOT NULL,
 status VARCHAR(255) NOT NULL,
 no_of_carts INT,
 manufacturer VARCHAR(255),
 PRIMARY KEY (train_id),

 -- Check that the status is one of "active" or "inactive"
 CHECK (status IN ('active', 'inactive')),
 -- Check that the capacity is positive
 CHECK (capacity > 0),
  -- Check that the number of carts is positive
 CHECK (no_of_carts > 0)
);

CREATE TABLE Trip
(
 trip_id INT NOT NULL IDENTITY(1,1),
 train_id INT NOT NULL,
 price FLOAT NOT NULL,
 start_date DATE NOT NULL,
 end_date DATE NOT NULL,
 start_time TIME NOT NULL, 
 end_time TIME NOT NULL,
 departure_station VARCHAR(255) NOT NULL,
 arrival_station VARCHAR(255) NOT NULL,
 PRIMARY KEY (trip_id),
 FOREIGN KEY (train_id) REFERENCES Train (train_id),

 -- Check that the start date is before the end date
 CHECK (start_date <= end_date),

 -- Check that the start time is before the end time
 CHECK (start_time < end_time)
);


CREATE TABLE Seat
(
 seat_id INT NOT NULL IDENTITY(1,1),
 trip_id INT NOT NULL,
 status VARCHAR(255) NOT NULL,
 PRIMARY KEY (seat_id, trip_id),
 FOREIGN KEY (trip_id) REFERENCES Trip (trip_id),

 -- Check that the status is one of "available" or "booked"
 CHECK (status IN ('available', 'booked'))
);


CREATE TABLE Booking
(
 booking_id INT NOT NULL IDENTITY(1,1),
 account_id INT NOT NULL,
 trip_id INT NOT NULL,
 no_of_seats INT NOT NULL,
 PRIMARY KEY (booking_id),
 FOREIGN KEY (account_id) REFERENCES Account (account_id),
 FOREIGN KEY (trip_id) REFERENCES Trip (trip_id),

 -- Check that the number of seats is positive
 CHECK (no_of_seats > 0)
);