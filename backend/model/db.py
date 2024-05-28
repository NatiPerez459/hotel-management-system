import psycopg2
import csv
from pathlib import Path

class Database:
    
    def __init__(self):
        self.credentials = self.connect()
        self.conn = psycopg2.connect(
            host = self.credentials['host'],
            database = self.credentials['database'],
            user = self.credentials['user'],
            password = self.credentials['password'],
            port = self.credentials['port']
        )
        
    def connect(self):
        path = Path(__file__).parent / '..' / '..' / 'credentials.csv'
        with open(str(path), 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            host, db, user, password, port = next(reader)
            db_dict = {'host': host, 'database': db, 'user': user, 'password': password, 'port': port}
            return db_dict
        
    def close(self):
        self.conn.close()