import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn

def create_table(conn, arg):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param arg: format of the table
    :return:
    """
    try:
        c = conn.cursor()
        stmt = "CREATE TABLE IF NOT EXISTS %s" % arg
        c.execute(stmt)
    except Error as e:
        print(e)

def create_student(conn, ID, first_name, last_name, highest=0):
    # Add user info into table Users
    try:
        c = conn.cursor()
        stmt = '''INSERT INTO Users(ID,First_name,Last_name,Highest_score)
                VALUES(?,?,?,?)'''
        c.execute(stmt, (ID, first_name, last_name, highest))
        conn.commit()
    except Error as e:
        print(e)

def create_record(conn, ID, Count, Date):
    # Add pull-up record into table Records
    try:
        c = conn.cursur()
        stmt = '''INSERT INTO Records(ID,Count,Date)
                VALURS(?,?,?)'''
        c.execute(stmt,(ID,Count,Date))
        conn.commit
        return 1
    except Error as e:
        print(e)
        return 0
