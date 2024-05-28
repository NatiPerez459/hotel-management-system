from backend.model.db import Database

class ChainsDAO:
    
    def __init__(self):
        self.db = Database()
        
    def getAllChains(self):
        cur = self.db.conn.cursor()
        query = """
                    SELECT * 
                    FROM Chains
                    WHERE chid >= 0;
                """
        cur.execute(query)
        chains_list = cur.fetchall()
        cur.close()
        self.db.close()
        return chains_list
    
    def getChainById(self, chid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT * 
                    FROM Chains
                    WHERE chid = %s;
                """
        cur.execute(query, [chid])
        chain = cur.fetchone()
        cur.close()
        self.db.close()
        return chain
    
    def addNewChain(self, cname, springmkup, summermkup, fallmkup, wintermkup):
        cur = self.db.conn.cursor()
        query = """
                    INSERT INTO Chains (cname, springmkup, summermkup, fallmkup, wintermkup) 
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *;
                """
        cur.execute(query, (cname, springmkup, summermkup, fallmkup, wintermkup))
        new_chain = cur.fetchone()  
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return new_chain 

    def updateChain(self, chid, cname, springmkup, summermkup, fallmkup, wintermkup):
        cur = self.db.conn.cursor()
        query = """
                    UPDATE Chains 
                    SET cname = %s, springmkup = %s, summermkup = %s, fallmkup = %s, wintermkup = %s 
                    WHERE chid = %s
                    RETURNING *;
                """
        cur.execute(query, (cname, springmkup, summermkup, fallmkup, wintermkup, chid))
        updated_chain = cur.fetchone() 
        self.db.conn.commit()
        cur.close()
        self.db.close()
        if updated_chain:
            return updated_chain
        else:
            return False

    
    def deleteChain(self, chid):
        cur = self.db.conn.cursor()
        query = """
                    DELETE FROM Chains 
                    WHERE chid = %s;
                """
        cur.execute(query, [chid])
        deleted_rows = cur.rowcount
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return deleted_rows != 0
