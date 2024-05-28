from backend.model.db import Database

class ClientDAO:
    
    def __init__(self):
        self.db = Database()
        
    def getAllClients(self):
        cur = self.db.conn.cursor()
        query = """
                    SELECT clid, fname, lname, age, memberyear
                    FROM Client;
                """
        cur.execute(query)
        clients_list = cur.fetchall()
        cur.close()
        self.db.close()
        return clients_list
    
    def getClientById(self, clid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT clid, fname, lname, age, memberyear
                    FROM Client 
                    WHERE clid = %s;
                """
        cur.execute(query, [clid])
        client = cur.fetchone()
        cur.close()
        self.db.close()
        return client
    
    def addNewClient(self, fname, lname, age, memberyear):
        cur = self.db.conn.cursor()
        query = """
                    INSERT INTO Client (fname, lname, age, memberyear) 
                    VALUES (%s, %s, %s, %s)
                    RETURNING *;
                """
        cur.execute(query, (fname, lname, age, memberyear))
        new_client = cur.fetchone() 
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return new_client  

    def updateClient(self, clid, fname, lname, age, memberyear):
        cur = self.db.conn.cursor()
        query = """
                    UPDATE Client
                    SET fname = %s, lname = %s, age = %s, memberyear = %s 
                    WHERE clid = %s
                    RETURNING *; 
                """
        cur.execute(query, (fname, lname, age, memberyear, clid))
        updated_client = cur.fetchone()
        self.db.conn.commit()
        cur.close()
        self.db.close()
        if updated_client:
            return updated_client 
        else:
            return False  

    
    def deleteClient(self, clid):
        cur = self.db.conn.cursor()
        query = """
                    DELETE FROM Client 
                    WHERE clid = %s;
                """
        cur.execute(query, [clid])
        deleted_rows = cur.rowcount
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return deleted_rows != 0