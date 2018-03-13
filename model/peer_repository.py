#!/usr/bin/env python

from database import database
from .Peer import Peer
from .File import File


def find_peer(conn: database.sqlite3.Connection, session_id: str) -> 'Peer':
	""" Retrive first peer from database

	Parameters:
		conn - the db connection
		session_id - session id for a peer

	Returns:
		peer - first matching result for the research
	"""
	c = conn.cursor()
	c.execute('SELECT * FROM peers WHERE session_id = ?', (session_id,))
	row = c.fetchone()

	if row is None:
		return None

	peer = Peer(session_id, row['ip'], row['port'])

	return peer


def find_file(conn: database.sqlite3.Connection, session_id: str, file_md5: str) -> 'File':
	""" Retrive first file from database

	Parameters:
		conn - the db connection
		session_id - session id for a peer
		file_md5 - md5 hash for a file

	Returns:
		file - first matching result for the research
	"""
	try:
		c = conn.cursor()
		c.execute(""" SELECT file_id FROM files
						NATURAL JOIN files_peers
						NATURAL JOIN peers
						WHERE session_id=?
						AND file_md5=? """, (session_id, file_md5,))
		(file_id, file_md5, file_name, download_count) = c.fetchone()
		file_data = File(file_id, file_md5, file_name, download_count)

	except database.Error as e:
		print(f'Errore: {e}')
		return None

	return file_data


def download_register(conn: database.sqlite3.Connection, session_id: str, file_md5: str) -> int:
	""" Register a new download for a file

	Parameters:
		conn - the db connection
		session_id - session id for a peer
		file_md5 - hash of the file

	Returns:
		int - number of downloads for that file
	"""
	try:
		c = conn.cursor()
		c.execute(""" SELECT * FROM peers
					NATURAL JOIN files_peers
					NATURAL JOIN files
					WHERE session_id = ? AND file_md5 = ? """, (session_id, file_md5))
		(file_id, file_md5, file_name, download_count) = c.fetchone()
		download_count += 1
		file = File(file_id, file_md5, file_name, download_count)
		file.update()

	except database.Error as e:
		print(f'Errore: {e}')
		return None

	return download_count
