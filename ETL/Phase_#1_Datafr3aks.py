import psycopg2
from utils import run_sql, insert_data
from pathlib import Path


def ETL_start(db_name : str, username : str, host : str, password : str):
    """
        This is the main function responsible for making the connection to postgres and 
        where the functions for table creation and data insertion are called from. 
        Credentials for the desired database are inputted through the CLI.

        Parameters:
            db_name : str -> The database you wish to connect to.
            username : str -> The username connected to the database.
            host : str -> The host where the database is located.
            password : str -> Password for the inputted user.

        Returns:
            None
    """

    try:
        #Connecting to database with the credentials provided
        with psycopg2.connect(dbname=db_name, user=username, host=host, password=password) as conn:
            
            print('Connected to PostgreSQL')
            with conn.cursor() as cur:
                
                #Drop all tables for complete reset (FOR TESTING ONLY)
                cur.execute("DROP TABLE IF EXISTS Chains, Hotel, Employee, Login, RoomDescription, Room, RoomUnavailable, Client, Reserve CASCADE;")
                run_sql(cur, str(Path(__file__).parent / 'create_tables.sql'))
                insert_data(cur)
                run_sql(cur, str(Path(__file__).parent / 'adjust_sequence.sql'))
                
            conn.commit()

    except (psycopg2.DatabaseError, Exception) as error:
        print('An error ocurred during the ETL process: ', error)

if __name__ == '__main__':
    print('----------Running DB phase 1------------')
    db_name = input('Input database name: ')
    host = input('Input host: ')
    username = input('Input username: ')
    password = input('Input username password: ')
    ETL_start(db_name, username, host, password)