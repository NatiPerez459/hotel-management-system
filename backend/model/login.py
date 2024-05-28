from backend.model.db import Database

class LoginDAO:
    
    def __init__(self):
        self.db = Database()
        
    def get_employee_id(self, username, password):
        cur = self.db.conn.cursor()
        query = """
                    SELECT eid 
                    FROM Login 
                    WHERE username = %s and password = %s;
                """
        cur.execute(query, (username, password))
        login = cur.fetchone()
        cur.close()
        self.db.close()
        return login
    
    def get_employee_position(self, eid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT position 
                    FROM Employee 
                    WHERE eid = %s;
                """
        cur.execute(query, [eid])
        position = cur.fetchone()[0]
        return position
    
    def get_employee_hotels(self, eid):
        cur = self.db.conn.cursor()
        position = self.get_employee_position(eid)
        if str(position).lower() == 'regular':
            query = """
                    SELECT hid 
                    FROM Employee 
                    WHERE eid = %s;
                """
            cur.execute(query, [eid])
            hotels = cur.fetchall()
        elif str(position).lower() == 'supervisor':
            query = """
                    SELECT chid
                    FROM  Hotel
                    NATURAL INNER JOIN Employee
                    WHERE eid = %s
                    """
            cur.execute(query, ([eid]))
            hotel_chain = cur.fetchone()[0]
            query = """
                    SELECT hid 
                    FROM Hotel
                    WHERE chid = %s;
                """
            cur.execute(query, [hotel_chain])
            hotels = cur.fetchall()
        elif str(position).lower() == 'administrator':
            query = """
                    SELECT hid 
                    FROM Hotel
                    WHERE hid != -1;
                """
            cur.execute(query)
            hotels = cur.fetchall()
        cur.close()
        self.db.close()
        return hotels
        
    def getAllLogin(self):
        cur = self.db.conn.cursor()
        query = """
                    SELECT lid, eid, username, password 
                    FROM Login;
                """
        cur.execute(query)
        login_list = cur.fetchall()
        cur.close()
        self.db.close()
        return login_list
    
    def getLoginById(self, lid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT lid, eid, username, password 
                    FROM Login 
                    WHERE lid = %s;
                """
        cur.execute(query, [lid])
        login = cur.fetchone()
        cur.close()
        self.db.close()
        return login
    
    def addNewLogin(self, eid, username, password):
        cur = self.db.conn.cursor()
        query = """
                    INSERT INTO Login (eid, username, password) 
                    VALUES (%s, %s, %s)
                    RETURNING *;
                """
        cur.execute(query, (eid, username, password))
        login = cur.fetchone()  
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return login
    
    def updateLogin(self, lid, eid, username, password):
        cur = self.db.conn.cursor()
        query = """
                    UPDATE Login 
                    SET eid = %s, username = %s, password = %s
                    WHERE lid = %s
                    RETURNING *;
                """
        cur.execute(query, (eid, username, password, lid))
        updated_login = cur.fetchone()
        self.db.conn.commit()
        cur.close()
        self.db.close()
        if updated_login:
            return updated_login  
        else:
            return False
    
    def deleteLogin(self, lid):
        cur = self.db.conn.cursor()
        query = """
                    DELETE FROM Login 
                    WHERE lid = %s;
                """
        cur.execute(query, [lid])
        deleted_rows = cur.rowcount
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return deleted_rows != 0