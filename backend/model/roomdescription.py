from backend.model.db import Database

class RoomDescriptionDAO:
    
    def __init__(self):
        self.db = Database()
        
    def getAllRoomDescriptions(self):
        cur = self.db.conn.cursor()
        query = """
                    SELECT rdid, rname, rtype, capacity, ishandicap 
                    FROM RoomDescription;
                """
        cur.execute(query)
        room_description_list = cur.fetchall()
        cur.close()
        self.db.close()
        return room_description_list
    
    def getRoomDescriptionById(self, rdid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT rdid, rname, rtype, capacity, ishandicap 
                    FROM RoomDescription 
                    WHERE rdid = %s;
                """
        cur.execute(query, [rdid])
        room_description = cur.fetchone()
        cur.close()
        self.db.close()
        return room_description
    
    def addNewRoomDescription(self, rname, rtype, capacity, ishandicap):
        cur = self.db.conn.cursor()
        query = """
                    INSERT INTO RoomDescription (rname, rtype, capacity, ishandicap) 
                    VALUES (%s, %s, %s, CAST( %s AS bool))
                    RETURNING *;
                """
        cur.execute(query, (rname, rtype, capacity, ishandicap))
        room_description = cur.fetchone()
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return room_description

    def updateRoomDescription(self, rdid, rname, rtype, capacity, ishandicap):
        cur = self.db.conn.cursor()
        query = """
                    UPDATE RoomDescription 
                    SET rname = %s, rtype = %s, capacity = %s, ishandicap = CAST( %s AS bool)
                    WHERE rdid = %s
                    RETURNING *;
                """
        cur.execute(query, (rname, rtype, capacity, ishandicap, rdid))
        updated_room_desc = cur.fetchone()
        self.db.conn.commit()
        cur.close()
        self.db.close()
        if updated_room_desc:
            return updated_room_desc  
        else:
            return False
    
    def deleteRoomDescription(self, rdid):
        cur = self.db.conn.cursor()
        query = """
                    DELETE FROM RoomDescription 
                    WHERE rdid = %s
                """
        cur.execute(query, [rdid])
        deleted_rows = cur.rowcount
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return deleted_rows != 0