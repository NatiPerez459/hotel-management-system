from flask import jsonify
from backend.model.db import Database

class LocalStatisticsDAO:

    def __init__(self):
        self.db = Database()
        
    def getEmployeePosition(self, eid):
        cur = self.db.conn.cursor()
        query = """SELECT position FROM Employee WHERE eid = %s;"""
        cur.execute(query, ([eid]))
        employee_position = cur.fetchone()[0]
        cur.close()
        self.db.close()
        return employee_position
    
    def getEmployeeHotel(self, eid):
        cur = self.db.conn.cursor()
        query = """
                SELECT hid 
                FROM Employee 
                NATURAL INNER JOIN Hotel
                WHERE eid = %s;
                """
        cur.execute(query, ([eid]))
        employee_hotel = cur.fetchone()
        cur.close()
        self.db.close()
        return employee_hotel
    
    def compareSupervisorChain(self, eid, hid):
        cur = self.db.conn.cursor()
        query = """
                SELECT chid
                FROM Employee
                NATURAL INNER JOIN Hotel
                WHERE eid = %s
                """
        cur.execute(query, ([eid]))
        employee_chain = cur.fetchone()[0]
        
        query = """
                    SELECT chid
                    FROM  Hotel
                    WHERE hid = %s
                    """
        cur.execute(query, ([hid]))
        hotel_chain = cur.fetchone()[0]
        
        return employee_chain == hotel_chain
    
    def getTopHandicapRooms(self, hid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT rid, COUNT(reid) AS total_reservations 
                    FROM RoomDescription 
                    NATURAL JOIN Room 
                    NATURAL JOIN RoomUnavailable 
                    NATURAL JOIN Reserve 
                    WHERE ishandicap = TRUE AND hid = %s
                    GROUP BY Room.rid 
                    ORDER BY total_reservations DESC 
                    LIMIT 5;
                """
        cur.execute(query, ([hid]))
        results = cur.fetchall()
        cur.close()
        self.db.close()
        return results
    
    def getTopRoomsWithLeastTimeUnavailable(self, hid):
        cur  = self.db.conn.cursor()
        query = """
                    SELECT rid, SUM(enddate-startdate) as total_days
                    FROM room
                    NATURAL JOIN roomunavailable
                    WHERE hid = %s
                    GROUP BY room.rid
                    ORDER BY total_days
                    LIMIT 3;
                """
        cur.execute(query, ([hid]))
        results = cur.fetchall()
        cur.close()
        self.db.close()
        return results
    
    def getTopClientsUnder30MostReservationsWithCreditCard(self, hid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT clid, age, COUNT(reid) as reservations
                    FROM Reserve
                    NATURAL JOIN Client
                    NATURAL JOIN Room
                    NATURAL JOIN RoomUnavailable
                    WHERE Reserve.payment = 'credit card' AND Client.age < 30 AND hid = %s
                    GROUP BY clid, age
                    ORDER BY reservations DESC
                    LIMIT 5
                """
        cur.execute(query, ([hid]))
        results = cur.fetchall()
        cur.close()
        self.db.close()
        return results
    
    def getTopHighestPaidRegularEmployees(self, hid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT eid, salary
                    FROM Employee
                    WHERE position = 'Regular' AND hid = %s
                    ORDER BY salary DESC
                    LIMIT 3;
                """
        cur.execute(query, ([hid]))
        results = cur.fetchall()
        cur.close()
        self.db.close()
        return results
    
    def TopClientsWithMostDiscounts(self, hid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT clid, fname, lname,
                        SUM(CASE
                                WHEN memberyear BETWEEN 1 AND 4 THEN total_cost * 0.02
                                WHEN memberyear BETWEEN 5 AND 9 THEN total_cost * 0.05
                                WHEN memberyear BETWEEN 10 AND 14 THEN total_cost * 0.08
                                WHEN memberyear >= 15 THEN total_cost * 0.12
                                ELSE 0
                            END
                        ) AS total_discount
                    FROM client NATURAL JOIN reserve NATURAL JOIN roomunavailable NATURAL JOIN room
                    WHERE hid = %s
                    GROUP BY clid, fname, lname
                    ORDER BY total_discount DESC
                    LIMIT 5;
                """
        cur.execute(query, ([hid]))
        results = cur.fetchall()
        cur.close()
        self.db.close()
        return results
    
    def TotalReservationsByRoomType(self, hid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT COUNT(*)
                    FROM reserve NATURAL JOIN roomunavailable NATURAL JOIN room
                    WHERE hid = %s;
                """
        cur.execute(query, ([hid]))
        total_count = cur.fetchone()

        query = """
                    SELECT rtype, COUNT(reid) AS total_reservations, (COUNT(reid) * 100.0 / %s) AS reservation_percentage
                    FROM reserve NATURAL JOIN roomunavailable NATURAL JOIN room NATURAL JOIN roomdescription
                    WHERE hid = %s
                    GROUP BY rtype;
                """
        cur.execute(query, ([total_count, hid]))
        results = cur.fetchall()

        cur.close()
        self.db.close()
        return results
    
    def TopRoomsWithLeastGuestToCapacityRatio(self, hid):
        cur = self.db.conn.cursor()
        query = """
                    SELECT rid, AVG(guests * 1.0 / capacity) AS guest_to_capacity_ratio
                    FROM reserve NATURAL JOIN roomunavailable NATURAL JOIN room NATURAL JOIN roomdescription
                    WHERE hid = %s
                    GROUP BY rid
                    ORDER BY guest_to_capacity_ratio
                    LIMIT 3;
                """
        cur.execute(query, ([hid]))
        results = cur.fetchall()
        cur.close()
        self.db.close()
        return results

