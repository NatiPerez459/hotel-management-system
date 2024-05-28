import pandas as pd
import sqlite3
import psycopg2
from pathlib import Path

def run_sql(postgres_cur : psycopg2.extensions.cursor, sql_file_path : str):
    try:
        with open(sql_file_path, 'r') as file:
            sql_commands = file.read()
            postgres_cur.execute(sql_commands)
    except (psycopg2.DatabaseError, Exception) as error:
        print('An error ocurred running sql file: ', error)

def insert_data(postgres_cur : psycopg2.extensions.cursor):
    """
        Responsible for data insertion. It goes file by file, extracting their contents
        and, with the provided postgres cursor, querying postsgres to insert the data/rows
        into their respective tables.

        Parameters:
            postgres_cur : psycopg2.extensions.cursor -> Cursor from the postgres-database connection.

        Returns:
            None
    """
    
    try:
        postgres_cur.executemany(
            query = "INSERT INTO Chains (chid, cname, springmkup, summermkup, fallmkup, wintermkup) VALUES(%s, %s, %s, %s, %s, %s)", 
            vars_list = extact_xlsx_data("chain.xlsx")
            )
        
        postgres_cur.executemany(
            query = "INSERT INTO Hotel (hid, chid, hname, hcity) VALUES(%s, %s, %s, %s)", 
            vars_list = extact_csv_data("hotel.csv")
            )
        
        postgres_cur.executemany(
            query = "INSERT INTO Employee (eid, hid, fname, lname, age, salary, position) VALUES(%s, %s, %s, %s, %s, %s, %s)", 
            vars_list = extact_json_data("employee.json")
            )
        
        postgres_cur.executemany(
            query = "INSERT INTO Login (lid, eid, username, password) VALUES(%s, %s, %s, %s)",
            vars_list = extact_xlsx_data("login.xlsx")
            )
        
        postgres_cur.executemany(
            query = "INSERT INTO RoomDescription (rdid, rname, rtype, capacity, ishandicap) VALUES(%s, %s, %s, %s, CAST(%s AS boolean))", 
            vars_list = extact_json_data("roomdetails.json")
            )
        
        postgres_cur.executemany(
            query = "INSERT INTO Room (rid, hid, rdid, rprice)  VALUES(%s, %s, %s, %s)", 
            vars_list = extact_db_data("rooms.db", "Room")
            )
        
        postgres_cur.executemany(
            query = "INSERT INTO RoomUnavailable (ruid, rid, startdate, enddate)  VALUES(%s, %s, %s, %s)", 
            vars_list = extact_csv_data("roomunavailable.csv")
            )
        
        postgres_cur.executemany(
            query = "INSERT INTO Client (clid, fname, lname, age, memberyear)  VALUES(%s, %s, %s, %s, %s)", 
            vars_list = extact_csv_data("client.csv")
            )
        
        postgres_cur.executemany(
            query = "INSERT INTO Reserve (reid, ruid, clid, total_cost, payment, guests) VALUES(%s, %s, %s, %s, %s, %s)", 
            vars_list = extact_db_data("reservations.db", "Reserve")
            )
    
    except (psycopg2.DatabaseError, Exception) as error:
        print('An error ocurred inserting data to tables: ', error)



"""
    The following functions are responsible for the extraction and processing
    of data from every file type in the provided Phase1_data file:
        - JSON
        - CSV
        - .xsls
        - .db (sqlite3)

"""
def extact_json_data(filename):
    try:
        path = str(Path(__file__).parent / '..' / 'Phase1_data' / filename)
        data = pd.read_json(path).dropna()
        return data.values.tolist()
    except:
        print("Failed to process json file.", path)

def extact_csv_data(filename):
    try:
        path = str(Path(__file__).parent / '..' / 'Phase1_data' / filename)
        data = pd.read_csv(path).dropna()
        return data.values.tolist()
    except:
        print("Failed to process csv file.", path)

def extact_xlsx_data(filename):
    try:
        path = str(Path(__file__).parent / '..' / 'Phase1_data' / filename)
        data = pd.read_excel(path).dropna()
        return data.values.tolist()
    except:
        print("Failed to process excel file.", path)

def extact_db_data(filename, table_name):
    try:
        path = str(Path(__file__).parent / '..' / 'Phase1_data' / filename)
        with sqlite3.connect(path) as conn:
            rows = conn.cursor().execute(" SELECT * FROM {}".format(table_name)).fetchall()
            return rows
    except (sqlite3.DatabaseError, Exception) as error:
        print('An error ocurred processing sqlite3 DB data: ', error, '\n', path)