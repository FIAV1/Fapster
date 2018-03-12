#!/usr/bin/env python

from Database import Database
from sqlite3 import Error


def main():
	db = Database().create_database()

	if db is not None:
		sql_create_files_table = """ CREATE TABLE IF NOT EXISTS files (
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
										file_id integer PRIMARY KEY,
										number char(5) NOT NULL,
										FOREIGN KEY (file_id) REFERENCES files (id) ON DELETE CASCADE
										);
										"""

		try:
			# create a database connection
			conn = Database().get_connection()
		except Error as e:
			print(e)
			exit(0)

		try:
			c = conn.cursor()
			# create files table
			c.execute(sql_create_files_table)
			# create peers table
			c.execute(sql_create_peers_table)
			# create downloads table
			c.execute(sql_create_downloads_table)
			# commits the statements
			conn.commit()
		except Error as e:
			conn.rollback()
			print(e)
			exit(0)

	else:
		print("Error: cannot create the database file.")


if __name__ == '__main__':
	main()
