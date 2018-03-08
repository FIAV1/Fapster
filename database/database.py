#!/usr/bin/env python

import sqlite3
from sqlite3 import Error

def createDatabase(dbFileName):
    """ create a sqlite db file
    :param dbFileName: database file name with path
    :return: String or None
    """
    try:
        dbFile = open(dbFileName, "w+")
        dbFile.close()
        return dbFileName
    except IOError as e:
        print(e)
    
    return None

def createConnection(dbFile):
    """ create a database connection to the SQLite database
        specified by dbFile
    :param dbFile: database file
    :return: Connection object or None
    """
    try:
        connection = sqlite3.connect(dbFile)
        return connection
    except Error as e:
        print(e)

    return None

def execQuery(conn, query):
    """ Execute a query
    :param conn: Connection object
    :param query: query to be executed
    :return: Boolean
    """
    try:
        c = conn.cursor()
        c.execute(query)
        return True
    except Error as e:
        print(e)
    
    return False
