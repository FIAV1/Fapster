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
	c = conn.cursor()
	c.execute('SELECT * FROM peers WHERE session_id = ?', (session_id,))
	row = c.fetchone()

	if row is None:
		return None

	peer = Peer(session_id, row['ip'], row['port'])

	return peer
