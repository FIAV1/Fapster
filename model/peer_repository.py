#!/usr/bin/env python

from database import database
from .Peer import Peer


def find(conn: database.sqlite3.Connection, session_id: str) -> 'Peer':
	""" Retrive first peer from database

	Parameters:
		conn - the db connection
		session_id - session id for a peer

	Returns:
		peer - first matching result for the research
	"""
	try:
		c = conn.cursor()
		c.execute('SELECT * FROM peers WHERE session_id = ?', (session_id,))
		(session_id, ip, port) = c.fetchone()
		peer = Peer(session_id, ip, port)

	except database.Error as e:
		print(f'Errore: {e}')
		return None

	return peer
