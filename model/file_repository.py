#!/usr/bin/env python

from database import database
from .File import File


def add_owner(conn: database.sqlite3.Connection, file_md5: str, peer_session_id: str) -> None:
	""" Add a file owner into the pivot table

	Parameters:
		conn - the db connection
		file_md5 - the md5 of the file
		session_id - the session id of the owner
	Returns:
		None
	"""
	conn.execute('INSERT INTO files_peers VALUES (?,?)', (file_md5, peer_session_id))


def find(conn: database.sqlite3.Connection, file_md5: str) -> 'File':
	""" Retrieve the file with the given md5 from database

	Parameters:
		conn - the db connection
		file_md5 - the md5 of the file

	Returns:
		file - the file found
	"""
	c = conn.cursor()
	c.execute('SELECT * FROM files WHERE file_md5 = ?', (file_md5,))
	row = c.fetchone()

	if row is None:
		return None

	file = File(file_md5, row['file_name'], row['download_count'])

	return file


def peer_has_file(conn: database.sqlite3.Connection, session_id: str, file_md5: str) -> bool:
	""" Retrieve the file with the given md5 from database

	Parameters:
		conn - the db connection
		file_md5 - the md5 of the file

	Returns:
		file - the file found
	"""
	c = conn.cursor()
	c.execute('SELECT * FROM files_peers WHERE file_md5=:md5 AND session_id=:id', {'md5': file_md5, 'id': session_id})
	row = c.fetchone()

	if row is None:
		return False

	return True


def get_copies(conn: database.sqlite3.Connection, file_md5: str) -> str:
	""" Retrieve the copies amount of the given file

	Parameters:
		conn - the db connection
		file_md5 - the md5 of the file

	Returns:
		int - the copies amount
	"""
	c = conn.cursor()
	c.execute('SELECT COUNT(file_md5) AS num FROM files_peers WHERE file_md5 = ?', (file_md5,))
	row = c.fetchone()

	if row is None:
		return None

	num = row['num']

	return num


def search(conn: database.sqlite3.Connection, query: str) -> str:
	""" Search the files with given string on the name

	Parameters:
		conn - the db connection
		query - keyword for the search

	Returns:
		file list - the list of corresponding files
	"""

	c = conn.cursor()
	c.execute('SELECT COUNT(file_md5) AS num FROM files WHERE file_name LIKE "%?%"', (query,))
	row = c.fetchone()

	if row is None:
		return None

	result = row['num']

	c.execute('SELECT file_md5, file_name FROM files WHERE file_name LIKE "%?%"', (query,))
	files = c.fetchall()

	if files is None:
		return None

	for file in files:
		file_md5 = file['file_md5']
		file_name = file['file_name']
		result = result + file_md5 + file_name + get_copies(conn, file_md5)
		c.execute('SELECT peers.ip, peers.port FROM files_peers JOIN peers ON files_peers.session_id = peers.session_id WHERE files_peers.file_md5 = ?', (file_md5,))
		peers = c.fetchall()

		if peers is None:
			return None
		for peer in peers:
			peer_ip = peer['peers.ip']
			peer_port = peer['peers.port']
			result = result + peer_ip + peer_port

	return result


def delete_peer_files(conn: database.sqlite3.Connection, session_id: str) -> int:
	""" Count all file that will be deleted by deleting the user

	Parameters:
		conn - the db connection
		session_id - session id for a peer

	Returns:
		int - amount of deleted files
	"""
	c = conn.cursor()
	c.execute('PRAGMA foreign_keys=ON')
	c.execute(""" DELETE FROM files
					WHERE file_md5 IN
						(SELECT f.file_md5
							FROM files AS f NATURAL JOIN files_peers AS f_p
							WHERE f_p.session_id=?
							AND f.file_md5 IN
								(SELECT file_md5
									FROM files_peers
									GROUP BY(file_md5)
									HAVING COUNT(file_md5) = 1)) """, (session_id,))
	deleted = c.execute('DELETE FROM files_peers WHERE session_id=?', (session_id,)).rowcount

	return deleted


def get_files_count_by_querystring(conn: database.sqlite3.Connection, query: str) -> int:
	""" Retrieve the number of files that match the query string
		Parameters:
			conn - the db connection
			query - keyword for the search
		Returns:
			int - the file amount
	"""

	c = conn.cursor()

	if query == '*':
		c.execute(
			'SELECT COUNT(file_md5) AS num '
			'FROM files'
		)
	else:
		c.execute(
			'SELECT COUNT(file_md5) AS num '
			'FROM files '
			'WHERE file_name LIKE ?',
			(query,)
		)

	row = c.fetchone()

	if row is None:
		return 0

	return row['num']


def get_files_with_copy_amount_by_querystring(conn: database.sqlite3.Connection, query: str) -> list:
	""" Retrieve the files matching the query string, with their copy amount
		Parameters:
			conn - the db connection
			query - keyword for the search
		Returns:
			file list - the list of corresponding files
	"""
	c = conn.cursor()

	if query == '*':
		c.execute(
			'SELECT f.file_md5, f.file_name, COUNT(f_p.file_md5) AS copies '
			'FROM files AS f NATURAL JOIN files_peers AS f_p '		
			'GROUP BY f_p.file_md5',
		)
	else:
		c.execute(
			'SELECT f.file_md5, f.file_name, COUNT(f_p.file_md5) AS copies '
			'FROM files AS f NATURAL JOIN files_peers AS f_p '
			'WHERE f.file_name LIKE ? '
			'GROUP BY f_p.file_md5',
			(query,)
		)

	file_rows = c.fetchall()

	return file_rows
