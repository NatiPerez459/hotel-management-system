from backend.model.db import Database
from flask import jsonify
from datetime import datetime
import math
#All verification methods go here 

def checkPaymentMethod(payment):
    allowed_methods = ['cash', 'check', 'credit card', 'debit card','pear pay']
    if payment in allowed_methods:
        return True
    return False

def checkRoomAvailabilty(rid, start, end):
    db = Database()
    cur = db.conn.cursor()
    query = """
            SELECT *
            FROM Roomunavailable
            WHERE rid = %s AND (startdate < %s AND enddate > %s) AND (startdate <> %s OR enddate <> %s)
            """
    cur.execute(query,([rid,end,start, start, end]))
    room_list = cur.fetchall()
    cur.close()
    db.close()
    if room_list:
        return False
    return True

def determineTotalCost(ruid, clid):
    db = Database()
    cur = db.conn.cursor()
    query = """
            SELECT memberyear
            FROM Client
            WHERE clid = %s;
            """
    cur.execute(query, ([clid]))
    member_year = cur.fetchone()[0]
    
    if member_year >= 1 and member_year <= 4:
        discount = 0.02
    elif member_year >= 5 and member_year <= 9:
        discount = 0.05
    elif member_year >= 10 and member_year <= 14:
        discount = 0.08
    elif member_year >= 15:
        discount = 0.12
    else:
        discount = 0
        
    query = """
            SELECT rprice
            FROM RoomUnavailable
            NATURAL INNER JOIN Room
            WHERE ruid = %s;
            """
    cur.execute(query, ([ruid]))
    room_price = cur.fetchone()[0]
    
    query = """
            SELECT REPLACE(TO_CHAR(startdate, 'Month'), ' ', '') AS month
            FROM RoomUnavailable
            WHERE ruid = %s;
            """
    cur.execute(query, ([ruid]))
    reservation_month = cur.fetchone()[0]
    
    if reservation_month in ['March', 'April', 'May']:
        mrkup_time = 'springmkup'
    elif reservation_month in ['June', 'July', 'August']:
        mrkup_time = 'summermkup'
    elif reservation_month in ['September', 'November', 'October']:
        mrkup_time = 'fallmkup'
    else:
        mrkup_time = 'wintermkup'
        
    query = """
            SELECT
            """ + mrkup_time + """
            FROM RoomUnavailable
            NATURAL INNER JOIN Room
            NATURAL INNER JOIN Hotel
            NATURAL INNER JOIN Chains
            WHERE ruid = %s;
            """
    cur.execute(query, ([ruid]))
    mrkup = cur.fetchone()[0]
    
    query = """
            SELECT enddate - startdate AS days
            FROM RoomUnavailable
            WHERE ruid = %s;
            """
    cur.execute(query, ([ruid]))
    total_days = cur.fetchone()[0]
    
    cur.close()
    db.close()

    return float(room_price) * float(total_days) * float(mrkup) * float(( float(1) - discount))
    
def handleLoginErrors(eid, username, password, lid=None):
    if None in [eid, username, password]:
        return jsonify("NULL values are invalid."), 404
    
    if not isinstance(eid, int):
        return jsonify("Eid must be int."), 404
    db = Database()
    cur = db.conn.cursor()
    query = """
            SELECT *
            FROM Employee
            WHERE eid = %s;
            """
    cur.execute(query, ([eid]))
    employee = cur.fetchone()
    if not employee:
        return jsonify("Employee does not exist."), 404

    query = """
            SELECT lid
            FROM Login
            WHERE eid = %s;
            """\
    
    cur.execute(query, ([eid]))
    employee_login = cur.fetchone()
    
    if employee_login:
        if lid is None:
            return jsonify("Employee already has a login."), 404
        elif employee_login[0] != lid:
            return jsonify(f"Employee is already linked to other credentials | lid={employee_login[0]}."), 404
    cur.close()
    db.close()
    
    if len(str(username)) > 50:
        return jsonify("Username is too long."), 404
    
    if len(str(password)) > 25:
        return jsonify("Password is too long."), 404
    return False

def handleLogOnErrors(username, password):
    if None in [username, password]:
        return jsonify("NULL values are invalid."), 404
    
    if len(str(username)) > 50:
        return jsonify("Username is too long."), 404
    
    if len(str(password)) > 25:
        return jsonify("Password is too long."), 404
    return False

def handleEmployeeErrors(hid, fname, lname, age, position, salary):
    if None in [hid, fname, lname, age, position, salary]:
        return jsonify("NULL values are invalid."), 404
    
    if not isinstance(hid, int):
        return jsonify("Hid must be int."), 404
    db = Database()
    cur = db.conn.cursor()
    query = """
            SELECT * 
            FROM Hotel
            WHERE hid = %s;
            """
    cur.execute(query, ([hid]))
    hotel = cur.fetchone()
    if not hotel:
        cur.close()
        db.close()
        return jsonify("Hotel does not exist."), 404
    cur.close()
    db.close()
    
    if not isinstance(fname, str):
        return jsonify("First name must be string."), 404
    if len(fname) > 50:
        return jsonify("First name is too long."), 404
    
    if not isinstance(lname, str):
        return jsonify("Last name must be string."), 404
    if len(lname) > 50:
        return jsonify("Last name is too long."), 404
    
    if not isinstance(age, int):
        return jsonify("Age must be int."), 404
    if age < 0:
        return jsonify("Age cannot be a negative number."), 404
    
    if str(position).lower() not in ['regular', 'supervisor', 'administrator']:
        return jsonify("The position is not valid."), 404
    
    if not isinstance(salary, float) and not isinstance(salary, int):
        return jsonify("Salary must be float or int."), 404
    if str(position).lower() == 'regular' and (salary > 49999 or salary < 18000):
        return jsonify("Incorrect salary for regular position."), 404
    if str(position).lower() == 'supervisor' and (salary > 79999 or salary < 50000):
        return jsonify("Incorrect salary for supervisor position."), 404
    if str(position).lower() == 'administrator' and (salary > 120000 or salary < 80000):
        return jsonify("Incorrect salary for administrator position."), 404
    return False

def handleChainErrors(cname, springmkup, summermkup, fallmkup, wintermkup):
    if None in [cname, springmkup, summermkup, fallmkup, wintermkup]:
        return jsonify("NULL values are invalid."), 404
    
    if not isinstance(cname, str):
        return jsonify("Chain name must be string."), 404
    if len(cname) > 50:
        return jsonify("Chain name is too long."), 404
    
    if not isinstance(springmkup, float) and not isinstance(springmkup, int):
        return jsonify("Springmkup must be float or int."), 404
    if springmkup < 0:
        return jsonify("Springmkup cannot be a negative number."), 404
    
    if not isinstance(summermkup, float) and not isinstance(summermkup, int):
        return jsonify("Summermkup must be float or int."), 404
    if summermkup < 0:
        return jsonify("Summermkup cannot be a negative number."), 404
    
    if not isinstance(fallmkup, float) and not isinstance(fallmkup, int):
        return jsonify("Fallmkup must be float or int."), 404
    if fallmkup < 0:
        return jsonify("Fallmkup cannot be a negative number."), 404
    
    if not isinstance(wintermkup, float) and not isinstance(wintermkup, int):
        return jsonify("Wintermkup must be float or int."), 404
    if wintermkup < 0:
        return jsonify("Wintermkup cannot be a negative number."), 404
    return False
    
def handleHotelErrors(chid, hname, hcity):
    if None in [chid, hname, hcity]:
        return jsonify("NULL values are invalid."), 404
    
    if not isinstance(chid, int):
        return jsonify("Chid must be int."), 404
    db = Database()
    cur = db.conn.cursor()
    query = """
            SELECT * 
            FROM Chains
            WHERE chid = %s;
            """
    cur.execute(query, ([chid]))
    chain = cur.fetchone()
    if not chain:
        cur.close()
        db.close()
        return jsonify("Chain does not exist."), 404
    cur.close()
    db.close()
    
    if not isinstance(hname, str):
        return jsonify("Hotel name must be string."), 404
    if len(hname) > 50:
        return jsonify("Hotel name is too long."), 404
    
    if not isinstance(hcity, str):
        return jsonify("City name must be string."), 404
    if len(hcity) > 25:
        return jsonify("City name is too long."), 404
    return False

def handleRoomErrors(hid, rdid, rprice):
    if None in [hid, rdid, rprice]:
        return jsonify("NULL values are invalid."), 404
    
    if not isinstance(hid, int):
        return jsonify("Hid must be int."), 404
    db = Database()
    cur = db.conn.cursor()
    query = """
            SELECT * 
            FROM Hotel
            WHERE hid = %s;
            """
    cur.execute(query, ([hid]))
    chain = cur.fetchone()
    if not chain:
        cur.close()
        db.close()
        return jsonify("Hotel does not exist."), 404
    
    if not isinstance(rdid, int):
        return jsonify("Rdid must be int."), 404
    query = """
            SELECT * 
            FROM RoomDescription
            WHERE rdid = %s
            """
    cur.execute(query, ([rdid]))
    room_description = cur.fetchone()
    if not room_description:
        cur.close()
        db.close()
        return jsonify("RoomDescription does not exist."), 404
    cur.close()
    db.close()
    
    if not isinstance(rprice, float) and not isinstance(rprice, int):
        return jsonify("Rprice must be float or int."), 404
    if rprice < 0:
        return jsonify("Rprice must not be negative."), 404
    return False

def handleRoomDescriptionErrors(rname, rtype, capacity, ishandicap):
    if None in [rname, rtype, capacity, ishandicap]:
        return jsonify("NULL values are invalid."), 404
    
    if not isinstance(ishandicap, bool) and ishandicap != 0 and ishandicap != 1:
        return jsonify("Ishandicap must be bool, 0, or 1."), 404
    
    valid_types = {
                    'standard': ['basic', 'premium'],
                    'standard queen': ['basic', 'premium', 'deluxe'],
                    'standard king': ['basic', 'premium', 'deluxe'],
                    'double queen': ['basic', 'premium', 'deluxe'],
                    'double king': ['premium', 'deluxe', 'suite'],
                    'triple king': ['deluxe', 'suite'],
                    'executive family': ['deluxe', 'suite'],
                    'presidential': ['suite']
                   }
    if str(rname).lower() not in valid_types.keys():
        return jsonify("Rname is not valid"), 404
    
    if str(rtype).lower() not in valid_types[str(rname).lower()]:
        return jsonify("Rtype is not valid."), 404
    
    valid_capacity = {
                    'standard': [1],
                    'standard queen': [1, 2],
                    'standard king': [2],
                    'double queen': [4],
                    'double king': [4, 6],
                    'triple king': [6],
                    'executive family': [4, 6, 8],
                    'presidential': [4, 6, 8]
                   }
    if not isinstance(capacity, int):
        return jsonify("Capacity must be int."), 404
    if capacity not in valid_capacity[str(rname).lower()]:
        return jsonify("Capacity is not valid."), 404
    return False

def handleRoomUnavailableErrors(rid, startdate, enddate):
    if None in [rid, startdate, enddate]:
        return jsonify("NULL values are invalid."), 404
    
    if not isinstance(rid, int):
        return jsonify("Rid must be int."), 404
    db = Database()
    cur = db.conn.cursor()
    query = """
            SELECT * 
            FROM Room
            WHERE rid = %s;
            """
    cur.execute(query, ([rid]))
    room = cur.fetchone()
    if not room:
        cur.close()
        db.close()
        return jsonify("Room does not exist."), 404
    cur.close()
    db.close()
    
    try:
        if datetime.strptime(startdate, '%Y-%m-%d').month > 12 or datetime.strptime(enddate, '%Y-%m-%d').month > 12:
            return jsonify("Startdate and Enddate must be in Year-month-day format."), 404
        if datetime.strptime(enddate, '%Y-%m-%d').month < 0 or datetime.strptime(enddate, '%Y-%m-%d').day < 0 or datetime.strptime(enddate, '%Y-%m-%d').year < 0:
            return jsonify("There must be no negatives in Year-month-day format."), 404
    except ValueError:
        return jsonify("Startdate and Enddate must be in Year-month-day format."), 404
    
    if not checkRoomAvailabilty(rid, startdate, enddate):
            return jsonify("Room can't be reserved at this time frame."), 422
    return False

def handleReserveErrors(ruid, clid, total_cost, payment, guests, reid=None):
    if None in [ruid, clid, total_cost, payment, guests]:
        return jsonify("NULL values are invalid."), 404
    
    if not isinstance(ruid, int):
        return jsonify("Ruid must be int."), 404
    db = Database()
    cur = db.conn.cursor()
    query = """
            SELECT reid 
            FROM Reserve
            WHERE ruid = %s;
            """
    cur.execute(query, ([ruid]))
    room_unavailable = cur.fetchone()
    if room_unavailable:
        if room_unavailable[0] >= 1 and room_unavailable[0] != reid:
            cur.close()
            db.close()
            return jsonify("Room is unavailable."), 404
    
    query = """
            SELECT * 
            FROM RoomUnavailable
            WHERE ruid = %s;
            """
    cur.execute(query, ([ruid]))
    room_un = cur.fetchone()
    if not room_un:
        return jsonify("Cannot reserve at this moment."), 404
    
    if not isinstance(clid, int):
        return jsonify("Clid must be int."), 404
    query = """
            SELECT * 
            FROM Client
            WHERE clid = %s;
            """
    cur.execute(query, ([clid]))
    client = cur.fetchone()
    if not client:
        cur.close()
        db.close()
        return jsonify("Client does not exist."), 404
    
    if not checkPaymentMethod(str(payment).lower()):
            return jsonify("Payment Method INVALID"), 422
        
    if not isinstance(guests, int):
        return jsonify("Guests must be int."), 404
    query = """
            SELECT capacity 
            FROM RoomUnavailable
            NATURAL INNER JOIN Room
            NATURAL INNER JOIN RoomDescription
            WHERE ruid = %s;
            """
    cur.execute(query, ([ruid]))
    max_capacity = cur.fetchone()[0]
    if guests > max_capacity:
        cur.close()
        db.close()
        return jsonify("More guests than room capacity entered."), 404
    
    if guests < 0:
        return jsonify("Guests cannot be negative."), 404
    
    correct_cost = round(float(determineTotalCost(ruid, clid)), 2)
    if not ((total_cost >= correct_cost-0.05) and (total_cost <= correct_cost+0.05)):
        return jsonify("Total cost is incorrect."), 404
    return False

def handleClientErrors(fname, lname, age, memberyear):
    if None in [fname, lname, age, memberyear]:
        return jsonify("NULL values are invalid."), 404
    
    if not isinstance(fname, str):
        return jsonify("First name must be string."), 404
    if len(fname) > 50:
        return jsonify("First name is too long."), 404
    
    if not isinstance(lname, str):
        return jsonify("Last name must be string."), 404
    if len(lname) > 50:
        return jsonify("Last name is too long."), 404
    
    if not isinstance(age, int):
        return jsonify("Age must be int."), 404
    if age < 0:
        return jsonify("Age cannot be a negative number."), 404
    
    if not isinstance(memberyear, int):
        return jsonify("Member year must be int."), 404
    if memberyear < 0:
        return jsonify("Member year cannot be a negative number."), 404
    return False
