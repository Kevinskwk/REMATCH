# Run this script in terminal to setup the database and/or add user info

import logging
import time
from sqlite_helper import create_connection, create_table, create_student

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Initiate sqlite database
conn = create_connection('database.sqlite')
print("Connected to database.sqlite")

# create users table
create_table(conn, '''Users (
                    ID integer PRIMARY KEY,
                    First_name text NOT NULL,
                    Last_name text,
                    Highest_score integer);''')
print("Created table Users")

# create records table
create_table(conn, '''Records (
                    Record_id integer PRIMARY KEY,
                    ID integer NOT NULL,
                    Count integer NOT NULL,
                    Date integer NOT NULL);''')
print("Created table Records")

def add_student(conn):
    try:
        ID = int(input("ID:"))
        First_name = str(input("First name:"))
        Last_name = str(input("Last name:"))
        create_student(conn,ID,First_name,Last_name)
        print("Created student ",ID)
        add_student(conn)
    except:
        print("Terminated")

print("input any none number in ID: to terminate")
add_student(conn)