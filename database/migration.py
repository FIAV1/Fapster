#!/usr/bin/env python

import database

def main():
    dbFileName = database.createDatabase("directory.db")

    if dbFileName is not None:

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
        conn = database.createConnection(dbFileName)
        if conn is not None:
            # create directory table
            database.execQuery(conn, sql_create_directory_table)
            # create peers table
            database.execQuery(conn, sql_create_peers_table)
            # create downloads table
            database.execQuery(conn, sql_create_downloads_table)

        else:
            print("Error! cannot create the database connection.")
    else: print("Error! cannot create the database file.")

if __name__ == '__main__':
    main()