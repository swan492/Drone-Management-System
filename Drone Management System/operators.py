
class Operator(object):
    """ Stores details on an operator. """

    def __init__(self):
        self.id = 0
        self.first_name = None
        self.family_name = None
        self.name = None
        self.date_of_birth = None
        self.drone_license = None
        self.rescue_endorsement = False
        self.operations = 0
        self.drone = None


class OperatorStore(object):
    """ Stores the operators. """

    def __init__(self, conn=None):
        self._conn = conn
    
    """ The following function is used to get all operators from the database"""
    def list(self):
        """ Fetch all the operators in the database. """
        
        cursor = self._conn.cursor()
        query = 'SELECT  CONCAT(o.FirstName, " ", o.LastName) name, dt.Types type, rt.Types rescue, o.Operations operations, CONCAT(d.ID, ": ", d.Name) drone'
        query += ' FROM OperatorStore o LEFT JOIN DroneStore d ON o.Drone = d.ID'
        query += ' LEFT JOIN DroneType dt ON o.DroneLicense = dt.ID'
        query += ' LEFT JOIN RescueType rt ON o.RescueEndorsement = rt.ID ORDER BY name'
        cursor.execute(query)
        for (name, type, rescue, operations, drone) in cursor:
            operator = Operator()
            operator.name = name
            operator.drone_license = type
            operator.rescue_endorsement = rescue
            operator.operations = operations
            operator.drone = drone
            yield operator
        cursor.close()

    """ The following function is used to add new operator to the database"""
    def add(self, operator):
        """ Adds a new operator to the database. """
        
        cursor = self._conn.cursor()
        query = 'INSERT INTO OperatorStore (FirstName, LastName, DroneLicense, RescueEndorsement, Operations) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(query, (operator.first_name, operator.family_name, operator.drone_license, operator.rescue_endorsement, operator.operations))
        cursor.close()
        self._conn.commit()
    
    """ The following function is used to get specific operator from the database"""
    def get(self, args):
        """ Retrieves a operator from the table by its name. """
        
        name = args.split(" ")
        cursor = self._conn.cursor()
        query = 'SELECT FirstName, LastName, DroneLicense, RescueEndorsement, Operations FROM OperatorStore WHERE FirstName = %s AND LastName = %s'
        cursor.execute(query, (name[0], name[-1]))
        for (FirstName, LastName, DroneLicense, RescueEndorsement, Operations) in cursor:
            operator = Operator()
            operator.first_name = FirstName
            operator.family_name = LastName
            operator.drone_license = DroneLicense
            operator.rescue_endorsement = RescueEndorsement
            operator.operations = Operations
        return operator
        cursor.close()
        
    
    """ The following function is used to update a operator in the database"""
    def save(self, operator):
        """ Update the operator to the database. """
        
        cursor = self._conn.cursor()
        query = 'UPDATE OperatorStore SET DroneLicense = %s, RescueEndorsement = %s, Operations = %s WHERE FirstName = %s AND LastName = %s'
        cursor.execute(query, (operator.drone_license, operator.rescue_endorsement, operator.operations, operator.first_name, operator.family_name))
        cursor.close()
        self._conn.commit()
        
