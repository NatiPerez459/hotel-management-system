from flask import jsonify
from backend.model.db import Database

class GlobalStatisticsDAO:
    
    def __init__(self):
        self.db = Database()
        
    def getEmployeePosition(self, eid):
        cur = self.db.conn.cursor()
        query = """SELECT position FROM Employee WHERE eid = %s;"""
        cur.execute(query, ([eid]))
        employee_position = cur.fetchone()
        cur.close()
        self.db.close()
        return employee_position
        
    def getMostReservations(self):
        cur = self.db.conn.cursor()
        query = """
                    SELECT hid, chid, hname, hcity, COUNT(*) AS reservations 
                    FROM hotel 
                    NATURAL INNER JOIN Room 
                    NATURAL INNER JOIN RoomUnavailable 
                    NATURAL INNER JOIN Reserve 
                    GROUP BY hid, chid, hname, hcity 
                    ORDER BY COUNT(*) DESC 
                    LIMIT (SELECT COUNT(hid) * 0.1 FROM hotel)
                """
        cur.execute(query)
        most_reservations = cur.fetchall()
        cur.close()
        self.db.close()
        return most_reservations
    
    def getMostProfitMoth(self):
        cur = self.db.conn.cursor()
        query = """
                    SELECT * 
                    FROM( 
                        SELECT chid, cname, REPLACE(TO_CHAR(startdate, 'Month'), ' ', '') AS month, COUNT(*) AS reservations, ROW_NUMBER() OVER(
                            PARTITION BY chid ORDER BY COUNT(*) DESC
                            ) 
                        FROM chains 
                        NATURAL INNER JOIN hotel 
                        NATURAL INNER JOIN room 
                        NATURAL INNER JOIN roomunavailable 
                        NATURAL INNER JOIN reserve 
                        GROUP BY chid, cname, month 
                        ORDER BY cname, COUNT(*) DESC 
                        ) AS data 
                    WHERE data.ROW_NUMBER in (1, 2, 3)
                """
        cur.execute(query)
        most_profit_month = cur.fetchall()
        cur.close()
        self.db.close()
        return most_profit_month
    
    def getHighestTotalRevenue(self):
        cur = self.db.conn.cursor()
        query = """
                    SELECT chid, cname, sum(total_cost) as revenue
                    FROM chains NATURAL JOIN hotel NATURAL JOIN room NATURAL JOIN roomunavailable NATURAL JOIN reserve 
                    GROUP BY chid, cname
                    ORDER BY revenue DESC
                    LIMIT 3;
                """
        cur.execute(query)
        highest_totalrev = cur.fetchall()
        print(highest_totalrev)
        cur.close()
        self.db.close()
        return highest_totalrev
    
    def getTotalRevPercByPayMethod(self):
        cur = self.db.conn.cursor()
        query = """
                    SELECT payment, count(payment)*1.0/(select count(reid) FROM reserve)*100 as percentage
                    FROM reserve 
                    GROUP BY payment;
                """
        cur.execute(query)
        total_percs = cur.fetchall()
        cur.close()
        self.db.close()
        return total_percs
    
    def getTop3ChainsLeastRooms(self):
        cur = self.db.conn.cursor()
        query = """
                    SELECT cname, count(*) AS total_rooms 
                    FROM chains NATURAL JOIN hotel NATURAL JOIN room 
                    GROUP BY chid 
                    ORDER BY total_rooms 
                    LIMIT 3;
                """
        cur.execute(query)
        chains = cur.fetchall()
        cur.close()
        self.db.close()
        return chains
    
    def getTop5HotelsMostCapacity(self):
        cur = self.db.conn.cursor()
        query = """
                    SELECT hname, SUM(capacity) AS total_capacity 
                    FROM hotel NATURAL JOIN room NATURAL JOIN roomdescription 
                    GROUP BY hid 
                    ORDER BY total_capacity DESC 
                    LIMIT 5;
                """
        cur.execute(query)
        hotels = cur.fetchall()
        cur.close()
        self.db.close()
        return hotels
    