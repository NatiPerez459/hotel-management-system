from backend.model.db import Database

class ReservationDAO:
    
    def __init__(self):
        self.db = Database()
        
    def getAllReservations(self):
        cur = self.db.conn.cursor()
        query = """
                    SELECT reid, ruid, clid, total_cost, payment, guests
                    FROM Reserve;
                """
        cur.execute(query)
        reservation_list = cur.fetchall()
        cur.close()
        self.db.close()
        return reservation_list
    
    def getReservationById(self, reid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT reid, ruid, clid, total_cost, payment, guests
                    FROM Reserve 
                    WHERE reid = %s;
                """
        cur.execute(query, [reid])
        reservation = cur.fetchone()
        cur.close()
        self.db.close()
        return reservation
    
    def addNewReservation(self, ruid, clid, total_cost, payment, guests): 
        cur = self.db.conn.cursor()
        query = """
                    INSERT INTO Reserve (ruid, clid, total_cost, payment, guests) 
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *;
                """
        cur.execute(query, (ruid, clid, total_cost, payment, guests))
        reservation = cur.fetchone()  
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return reservation
    
    def updateReservation(self, reid, ruid, clid, total_cost, payment, guests): 
        cur = self.db.conn.cursor()
        query = """
                    UPDATE Reserve 
                    SET ruid = %s, clid = %s, total_cost = %s, payment = %s, guests = %s
                    WHERE reid = %s
                    RETURNING *;
                """
        cur.execute(query, (ruid, clid, total_cost, payment, guests,reid))
        updated_reservation = cur.fetchone()
        self.db.conn.commit()
        cur.close()
        self.db.close()
        if updated_reservation:
            return updated_reservation  
        else:
            return False
    
    def deleteReservation(self, reid):
        cur = self.db.conn.cursor()
        query = """
                    DELETE FROM Reserve 
                    WHERE reid = %s;
                """
        cur.execute(query, [reid])
        deleted_rows = cur.rowcount
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return deleted_rows != 0