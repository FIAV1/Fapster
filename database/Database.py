#!/usr/bin/env python

import sqlite3
from sqlite3 import Error
from typing import Union


class Database:

    def __init__(self):
        self.DB_FILE = "directory.db"

    def create_database(self):
        """ Create a sqlite db file

        Returns:
            str - a string containing the db name, or None
        """
        try:
            db_file = open(self.DB_FILE, "w+")
            db_file.close()
            return self.DB_FILE
        except IOError as e:
            print(e)

        return None

    def get_connection(self):
        """ create a database connection to the SQLite database specified by DB_FILE

        Returns:
            Connection - Connection object or None
        """
        try:
            connection = sqlite3.connect(self.DB_FILE)
            return connection
        except Error as e:
            print(e)

        return None
