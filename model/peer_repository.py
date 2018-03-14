#!/usr/bin/env python

from database import database
from .Peer import Peer
from .File import File


def find(conn: database.sqlite3.Connection, session_id: str) -> 'Peer':
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


def get_deleted(conn: database.sqlite3.Connection, session_id: str) -> int:
	""" Count all file that will be deleted by deleting the user

	Parameters:
		conn - the db connection
		session_id - session id for a peer

	Returns:
		int - amount of deleted files
	"""
	c = conn.cursor()
	c.execute('SELECT COUNT(session_id) AS num FROM files_peers WHERE session_id = ?', (session_id,))
	row = c.fetchone()

	if row is None:
		return None

	num = row['num']

	return num


def file_unlink(conn: database.sqlite3.Connection, session_id: str, file_md5: str) -> bool:
	""" Unlink the Peer from the file

	Parameters:
		conn - the db connection
		session_id - session id for a peer
		file_md5 - md5 hash of a file

	Returns:
		bool - true or false either if it succeds or fails
	"""

	c = conn.cursor()
	row = c.execute('DELETE FROM files_peers WHERE file_md5=? AND session_id=?', (file_md5, session_id,)).rowcount

	if row <= 0:
		return False

	return True
