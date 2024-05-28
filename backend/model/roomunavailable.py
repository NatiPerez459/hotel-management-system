from backend.model.db import Database

class RoomUnavailableDAO:
    
    def __init__(self):
        self.db = Database()

    def getAllRoomUnavailable(self):
        cur = self.db.conn.cursor()
        query = """
                    SELECT ruid, rid, startdate, enddate 
                    FROM RoomUnavailable;
                """
        cur.execute(query)
        room_unavailable_list = cur.fetchall()
        cur.close()
        self.db.close()
        return room_unavailable_list
    
    def getRoomUnavailableById(self, ruid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT ruid, rid, startdate, enddate 
                    FROM RoomUnavailable 
                    WHERE ruid = %s;
                """
        cur.execute(query, [ruid])
        room_unavailable = cur.fetchone()
        cur.close()
        self.db.close()
        return room_unavailable
    
    def addNewRoomUnavailable(self, rid, startdate, enddate):
        cur = self.db.conn.cursor()
        query = """
                    INSERT INTO RoomUnavailable (rid, startdate, enddate) 
                    VALUES (%s, %s, %s)
                    RETURNING *;
                """
        cur.execute(query, (rid, startdate, enddate))
        room_unavailable = cur.fetchone()
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return room_unavailable

    def updateRoomUnavailable(self, ruid, rid, startdate, enddate):
        cur = self.db.conn.cursor()
        query = """
                    UPDATE RoomUnavailable 
                    SET rid = %s, startdate = %s, enddate = %s 
                    WHERE ruid = %s
                    RETURNING *;
                """
        cur.execute(query, (rid, startdate, enddate, ruid))
        updated_room_unav = cur.fetchone()
        self.db.conn.commit()
        cur.close()
        self.db.close()
        if updated_room_unav:
            return updated_room_unav  
        else:
            return False
    
    def deleteRoomUnavailable(self, ruid):
        cur = self.db.conn.cursor()
        query = """
                    DELETE FROM RoomUnavailable 
                    WHERE ruid = %s
                """
        cur.execute(query, [ruid])
        deleted_rows = cur.rowcount
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return deleted_rows != 0