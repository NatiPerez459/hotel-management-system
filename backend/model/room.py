from backend.model.db import Database

class RoomDAO:
    
    def __init__(self):
        self.db = Database()
        
    def getAllRooms(self):
        cur = self.db.conn.cursor()
        query = """
                    SELECT rid, hid, rdid, rprice 
                    FROM Room;
                """
        cur.execute(query)
        rooms_list = cur.fetchall()
        cur.close()
        self.db.close()
        return rooms_list
    
    def getRoomById(self, rid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT rid, hid, rdid, rprice 
                    FROM Room 
                    WHERE rid = %s;
                """
        cur.execute(query, [rid])
        room = cur.fetchone()
        cur.close()
        self.db.close()
        return room
    
    def addNewRoom(self, hid, rdid, rprice):
        cur = self.db.conn.cursor()
        query = """
                    INSERT INTO Room (hid, rdid, rprice) 
                    VALUES (%s, %s, %s)
                    RETURNING *;
                """
        cur.execute(query, (hid, rdid, rprice))
        room = cur.fetchone()  
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return room
    
    def updateRoom(self, rid, hid, rdid, rprice):
        cur = self.db.conn.cursor()
        query = """
                    UPDATE Room 
                    SET hid = %s, rdid = %s, rprice = %s 
                    WHERE rid = %s
                    RETURNING *;
                """
        cur.execute(query, (hid, rdid, rprice, rid))
        updated_room = cur.fetchone()
        self.db.conn.commit()
        cur.close()
        self.db.close()
        if updated_room:
            return updated_room  
        else:
            return False

    
    def deleteRoom(self, rid):
        cur = self.db.conn.cursor()
        query = """
                    DELETE FROM Room 
                    WHERE rid = %s;
                """
        cur.execute(query, [rid]) 
        deleted_rows = cur.rowcount
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return deleted_rows != 0
        