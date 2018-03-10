#!/usr/bin/env python

import database


def main():
	db_file_name = database.create_database()

	if db_file_name is not None:

		sql_create_directory_table = """ CREATE TABLE IF NOT EXISTS files (
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
										id integer PRIMARY KEY,
										file_id integer
										number char(5) NOT NULL,
										FOREIGN KEY (file_id) REFERENCES directory (file_id) ON DELETE CASCADE
										);
										"""

		try:
			# create a database connection
			conn = database.get_connection()
		except database.Error as e:
			print(e)
			exit(0)

		try:
			c = conn.cursor()
			# create directory table
			c.execute(sql_create_directory_table)
			# create peers table
			c.execute(sql_create_peers_table)
			# create downloads table
			c.execute(sql_create_downloads_table)
			# commits the statements
			conn.commit()
		except database.Error as e:
			conn.rollback()
			print(e)
			exit(0)

	else:
		print("Error: cannot create the database file.")


if __name__ == '__main__':
	main()
