from backend.model.db import Database

class EmployeeDAO:
    
    def __init__(self):
        self.db = Database()
        
    def getAllEmployees(self):
        cur = self.db.conn.cursor()
        query = "SELECT * FROM Employee;"
        cur.execute(query)
        employees_list = cur.fetchall()
        cur.close()
        self.db.close()
        return employees_list
    
    def getEmployeeById(self, eid):
        cur = self.db.conn.cursor()
        query = "SELECT * FROM Employee WHERE eid = %s;"
        cur.execute(query, [eid])
        employee = cur.fetchone()
        cur.close()
        self.db.close()
        return employee
    
    def addNewEmployee(self, hid, fname, lname, age, position, salary):
        cur = self.db.conn.cursor()
        query = """
                    INSERT INTO Employee (hid, fname, lname, age, position, salary) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING *;
                """
        cur.execute(query, (hid, fname, lname, age, position, salary))
        added_employee = cur.fetchone()
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return added_employee
    
    def updateEmployee(self, eid, hid, fname, lname, age, position, salary):
        cur = self.db.conn.cursor()
        query = """
                    UPDATE Employee 
                    SET hid = %s, fname = %s, lname = %s, age = %s, position = %s, salary = %s
                    WHERE eid = %s
                    RETURNING *;
                """
        cur.execute(query, (hid, fname, lname, age, position, salary, eid))
        updated_employee = cur.fetchone()
        self.db.conn.commit()
        cur.close()
        self.db.close()
        if updated_employee:
            return updated_employee  
        else:
            return False
    
    def deleteEmployee(self, eid):
        cur = self.db.conn.cursor()
        query = "DELETE FROM Employee WHERE eid = %s;"
        cur.execute(query, [eid])
        deleted_rows = cur.rowcount
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return deleted_rows != 0
