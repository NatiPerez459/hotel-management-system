from backend.model.db import Database

class HotelDAO:
    
    def __init__(self):
        self.db = Database()
        
    def getAllHotels(self):
        cur = self.db.conn.cursor()
        query = """
                    SELECT * 
                    FROM Hotel
                    WHERE hid >= 0;
                """
        cur.execute(query)
        hotels_list = cur.fetchall()
        cur.close()
        self.db.close()
        return hotels_list
    
    def getHotelById(self, hid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT * 
                    FROM Hotel
                    WHERE hid = %s;
                """
        cur.execute(query, [hid])
        hotel = cur.fetchone()
        cur.close()
        self.db.close()
        return hotel
    
    def addNewHotel(self, chid, hname, hcity):
        cur = self.db.conn.cursor()
        query = """
                    INSERT INTO Hotel (chid, hname, hcity) 
                    VALUES (%s, %s, %s)
                    RETURNING *;
                """
        cur.execute(query, (chid, hname, hcity))
        hotel = cur.fetchone()  
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return hotel
    
    def updateHotel(self, hid, chid, hname, hcity):
        cur = self.db.conn.cursor()
        query = """
                    UPDATE Hotel 
                    SET chid = %s, hname = %s, hcity = %s 
                    WHERE hid = %s
                    RETURNING *;
                """
        cur.execute(query, (chid, hname, hcity, hid))
        updated_hotel = cur.fetchone()
        self.db.conn.commit()
        cur.close()
        self.db.close()
        if updated_hotel:
            return updated_hotel  
        else:
            return False
    
    def deleteHotel(self, hid):
        cur = self.db.conn.cursor()
        query = """
                    DELETE FROM Hotel 
                    WHERE hid = %s;
                """
        cur.execute(query, [hid])
        deleted_rows = cur.rowcount
        self.db.conn.commit()
        cur.close()
        self.db.close()
        return deleted_rows != 0
