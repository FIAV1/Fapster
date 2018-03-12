#!/usr/bin/env python

import sqlite3
from sqlite3 import Error
import os.path

DB_FILE = "directory.db"

def exist():
	if os.path.exists(DB_FILE):
		return True
	return False

def create_database():
	""" Create a sqlite db file

	Returns:
		str - a string containing the db name, or None
	"""
	try:
		db_file = open(DB_FILE, "w+")

		if db_file is not None:
			sql_create_peers_table = """ CREATE TABLE IF NOT EXISTS peers (									
											session_id char(16) PRIMARY KEY,
											ip char(55) NOT NULL,
											port char(5) NOT NULL
											);
											"""

			sql_create_files_table = """ CREATE TABLE IF NOT EXISTS files (
												id integer PRIMARY KEY,										
												file_md5 char(32) NOT NULL,
												file_name char(100) NOT NULL,
												download_count integer DEFAULT 0										
												);
												"""

			sql_create_files_peers_table = """ CREATE TABLE IF NOT EXISTS files_peers (
												file_id integer NOT NULL,
												peer_session_id char(16) NOT NULL,	
												PRIMARY KEY (file_id, peer_session_id),
												FOREIGN KEY (file_id) REFERENCES files (id) ON DELETE CASCADE,
												FOREIGN KEY (peer_session_id) REFERENCES peers (session_id) ON DELETE CASCADE																
												);
												"""

			try:
				# create a database connection
				conn = get_connection()
			except Error as e:
				print(e)
				exit(0)

			try:
				c = conn.cursor()
				# create files table
				c.execute(sql_create_files_table)
				# create peers table
				c.execute(sql_create_peers_table)
				# create files_peers table
				c.execute(sql_create_files_peers_table)
				# enable the foreign keys
				c.execute('PRAGMA foreign_keys = ON;')
				# commits the statements
				conn.commit()
			except Error as e:
				conn.rollback()
				print(e)
				exit(0)

		else:
			print("Error: cannot create the database file.")
	except IOError as e:
		print(e)


def refresh_databse():

	statements = 'DELETE FROM peers; DELETE FROM files; DELETE FROM files_peers; PRAGMA foreign_keys = ON;'

	try:
		# create a database connection
		conn = get_connection()
	except Error as e:
		print(e)
		exit(0)

	try:
		c = conn.cursor()
		# delete all tables content
		c.executescript(statements)
		# commits the statement
		conn.commit()
	except Error as e:
		conn.rollback()
		print(e)
		exit(0)


def get_connection():
	""" create a database connection to the SQLite database specified by DB_FILE

	Returns:
		Connection - Connection object or None
	"""
	try:
		return sqlite3.connect(DB_FILE)
	except Error as e:
		print(e)
