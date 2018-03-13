#!/usr/bin/env python

from database import database


class File:

	def __init__(self, file_md5, file_name, download_count):
		self.file_md5 = file_md5
		self.file_name = file_name
		self.download_count = download_count

	def insert(self, conn: database.sqlite3.Connection) -> None:
		""" Insert a file into db

		Parameters:
			conn - the db connection
			peer_session_id - the session id of the peer who want to add the file
		Returns:
			None
		"""
		conn.execute('INSERT INTO files VALUES (?,?,?)', (self.file_md5, self.file_name, self.download_count))

	def update(self, conn: database.sqlite3.Connection) -> None:
		""" Delete a peer from db

		Parameters:
			conn - the db connection
			peer_session_id - the session id of the peer who want to add the file
		Returns:
			None
		"""
		query = """UPDATE files
		SET file_name=:name, download_count=:count
		WHERE file_md5 =:md5"""

		conn.execute(query, {'md5': self.file_md5, 'name': self.file_name, 'count': self.download_count})

	def delete(self, conn: database.sqlite3.Connection) -> int:
		""" Delete a peer from db

		Parameters:
			conn - the db connection
		Returns:
			int - number of file deleted, owned by the peer
		"""
		conn.execute('DELETE FROM files WHERE file_md5 = ?', (self.file_md5,))

