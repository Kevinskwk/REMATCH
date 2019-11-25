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

def create_user(conn, ID, first_name, last_name, highest=0, total=0):
    # Add user info into table Users
    try:
        c = conn.cursor()
        stmt = '''INSERT INTO Users(ID,First_name,Last_name,Highest,Total)
                VALUES(?,?,?,?,?)'''
        c.execute(stmt, (ID, first_name, last_name, highest, total))
        conn.commit()
    except Error as e:
        print(e)

def create_record(conn, ID, Count, Date):
    # Add pull-up record into table Records
    try:
        c = conn.cursur()
        stmt = '''INSERT INTO Records(ID,Count,Year,Month,Day)
                VALUES(?,?,?,?,?)'''
        c.execute(stmt,(ID,Count,Date[0],Date[1],Date[2]))
        conn.commit
        return 1
    except Error as e:
        print(e)
        return 0

def edit_user(conn, ID, first_name, last_name):
    try:
        c = conn.cursor()
        stmt = '''UPDATE Users
                SET First_name = ?,
                    Last_name = ?
                WHERE ID = ?'''
        c.execute(stmt, (first_name, last_name, ID))
        conn.commit()
    except Error as e:
        print(e)

def user_info(conn, ID):
    try:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        stmt = '''SELECT * FROM Users WHERE ID=?'''
        c.execute(stmt,(ID,))
        #c.commit()
        rows = c.fetchall()
        info={}
        for row in rows:
            info.update(dict(row))
        return info
    except Error as e:
        print(e)

def update_score(conn, ID, count):
    try:
        c = conn.cursor()
        stmt = '''UPDATE Users
                SET Total = Total + ?,
                    Highest = MAX(Highest, ?)
                WHERE ID = ?;
                '''
        c.execute(stmt,(count,count,ID))
        c.commit()
    except Error as e:
        print(e)