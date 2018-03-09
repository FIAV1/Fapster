#!/usr/bin/env python

import sqlite3
from sqlite3 import Error
from typing import Union

DB_FILE = "directory.db"


def create_database() -> Union[str, None]:
    """ create a sqlite db file
    :return: str or None
    """
    try:
        db_file = open(DB_FILE, "w+")
        db_file.close()
        return DB_FILE
    except IOError as e:
        print(e)
    
    return None


def get_connection() -> Union[sqlite3.Connection, None]:
    """ create a database connection to the SQLite database
        specified by dbFile
    :return: Connection object or None
    """
    try:
        connection = sqlite3.connect(DB_FILE)
        return connection
    except Error as e:
        print(e)

    return None
