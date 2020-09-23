-- Initialise DroneType table
CREATE TABLE DroneType (
	ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	Types VARCHAR(100) NOT NULL
);

-- Initialise RescueType table
CREATE TABLE RescueType (
	ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	Types VARCHAR(100) NOT NULL
);

-- Initialise DroneStore table
CREATE TABLE DroneStore (
	ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	Name VARCHAR(100) NOT NULL,
	ClassType INT NOT NULL,
	Rescue INT NOT NULL,
	Operators INT,
	FOREIGN KEY (ClassType) REFERENCES DroneType(ID),
	FOREIGN KEY (Rescue) REFERENCES RescueType(ID)
);

-- Initialise OperatorStore table
CREATE TABLE OperatorStore (
	ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	FirstName VARCHAR(100) NOT NULL,
	LastName VARCHAR(100) NOT NULL,
	DOB DATE,
	DroneLicense INT,
	RescueEndorsement INT,
	Operations INT,
	Drone INT,
	FOREIGN KEY (DroneLicense) REFERENCES DroneType(ID),
	FOREIGN KEY (RescueEndorsement) REFERENCES RescueType(ID),
	FOREIGN KEY (Drone) REFERENCES DroneStore(ID)
);

-- Add foreign key to DroneStore table
ALTER TABLE DroneStore
ADD FOREIGN KEY (Operators) REFERENCES OperatorStore(ID);



	