
class Drone(object):
    """ Stores details on a drone. """

    def __init__(self, name, class_type=1, rescue=False):
        self.id = 0
        self.name = name
        self.class_type = class_type
        self.rescue = rescue
        self.operator = None



class DroneStore(object):
    """ DroneStore stores all the drones for DALSys. """

    def __init__(self, conn=None):
        self._conn = conn
        
    """ The following function is used to get all drones from the database"""
    def list(self):
        """ Fetch all the drones in the database. """
        
        cursor = self._conn.cursor()
        query = 'SELECT d.ID id, d.Name name, dt.Types type, rt.Types rescue, CONCAT(o.FirstName, " ", o.LastName) operator'
        query += ' FROM DroneStore d LEFT JOIN OperatorStore o ON d.Operators = o.ID'
        query += ' INNER JOIN DroneType dt ON dt.ID = d.ClassType'
        query += ' INNER JOIN RescueType rt ON rt.ID = d.Rescue ORDER BY name'
        cursor.execute(query)
        for (id, name, type, rescue, operator) in cursor:
            drone = Drone(name, type, rescue)
            drone.id = id
            drone.operator = operator
            yield drone
        cursor.close()
    
    """ The following function is used to add new drone to the database"""
    def add(self, drone):
        """ Adds a new drone to the database. """
        
        cursor = self._conn.cursor()
        query = 'INSERT INTO DroneStore (Name, ClassType, Rescue) VALUES (%s, %s, %s)'
        cursor.execute(query, (drone.name, drone.class_type, drone.rescue))
        cursor.close()
        self._conn.commit()
        
    """ The following function is used to get specific drone from the database"""
    def get(self, id):
        """ Retrieves a drone from the Drone table by its ID. """
        
        cursor = self._conn.cursor()
        query = 'SELECT d.ID id, d.Name name, d.ClassType type, d.Rescue rescue, CONCAT(o.FirstName, " ", o.LastName) operator '
        query += 'FROM DroneStore d LEFT JOIN OperatorStore o ON d.Operators = o.ID WHERE d.ID = ' + str(id)
        cursor.execute(query)
        for (id, name, type, rescue, operator) in cursor:
            drone = Drone(name, type, rescue)
            drone.id = id
            drone.operator = operator
        return drone
        cursor.close()

    """ The following function is used to update a drone in the database"""
    def save(self, drone):
        """ Update the drone to the database. """
        
        cursor = self._conn.cursor()
        query = 'UPDATE DroneStore SET Name = %s, ClassType = %s, Rescue = %s WHERE ID = %s'
        cursor.execute(query, (drone.name, drone.class_type, drone.rescue, drone.id))
        cursor.close()
        self._conn.commit()
    