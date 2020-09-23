
-- Add DroneType records with two types
INSERT INTO DroneType (Types)
VALUES ("One");

INSERT INTO DroneType (Types)
VALUES ("Two");

-- Add RescueType records with two types
INSERT INTO RescueType (Types)
VALUES ("No");

INSERT INTO RescueType (Types)
VALUES ("Yes");

-- Add an operator without a valid drone license
INSERT INTO OperatorStore (FirstName, LastName, DOB, RescueEndorsement)
VALUES ("Op", "One", "1995-11-30", 1);

-- Add an operator with a class 1 drone license
INSERT INTO OperatorStore (FirstName, LastName, DOB, DroneLicense, RescueEndorsement, Operations, Drone)
VALUES ("Op", "Two", "1990-12-30", 1, 1, 3, 4);

-- Add an operator with a class 2 drone license
INSERT INTO OperatorStore (FirstName, LastName, DOB, DroneLicense, RescueEndorsement, Operations, Drone)
VALUES ("Op", "Three", "1991-10-30", 2, 1, 0, 5);

-- Add an operator with a rescue endorsement and a valid drone license
INSERT INTO OperatorStore (FirstName, LastName, DOB, DroneLicense, RescueEndorsement, Operations)
VALUES ("Op", "Four", "1994-12-30", 1, 2, 9);

-- Add a class 1 search drone
INSERT INTO DroneStore (Name, ClassType, Rescue)
VALUES ("Drone1", 1, 1);

-- Add a class 2 search drone
INSERT INTO DroneStore (Name, ClassType, Rescue)
VALUES ("Drone2", 2, 1);

-- Add a rescue drone
INSERT INTO DroneStore (Name, ClassType, Rescue)
VALUES ("Drone3", 1, 2);

-- Add two drones allocated to valid operators
INSERT INTO DroneStore (Name, ClassType, Rescue, Operators)
VALUES ("Drone4", 1, 1, 2);

INSERT INTO DroneStore (Name, ClassType, Rescue, Operators)
VALUES ("Drone5", 2, 1, 3);


