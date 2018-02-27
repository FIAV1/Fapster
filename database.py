import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

	
def main():
    database = "directory.db"
 
    sql_create_directory_table = """ CREATE TABLE IF NOT EXISTS directory (
                                        id integer PRIMARY KEY,
                                        file_md5 char(32) NOT NULL,
                                        file_name char(100) NOT NULL,
                                        session_id char(16) NOT NULL,
                                        FOREIGN KEY (session_id) REFERENCES peers (session_id) ON DELETE CASCADE
                                        );
                                    """
 
    sql_create_peers_table = """ CREATE TABLE IF NOT EXISTS peers (
                                    session_id char(16) PRIMARY KEY,
                                    ip char(55) NOT NULL,
                                    port char(5) NOT NULL
                                    );
                                """

    sql_create_downloads_table = """ CREATE TABLE IF NOT EXISTS downloads (
                                    file_md5 char(32) PRIMARY KEY,
                                    number char(5) NOT NULL,
                                    FOREIGN KEY (file_md5) REFERENCES directory (file_md5) ON DELETE CASCADE
                                    );
                                """
 
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create directory table
        create_table(conn, sql_create_directory_table)
        # create peers table
        create_table(conn, sql_create_peers_table)
        # create downloads table
        create_table(conn, sql_create_downloads_table)

    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()