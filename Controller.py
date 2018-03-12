#!/usr/bin/env python

from model.Peer import Peer
import uuid


class Controller:

	@staticmethod
	def login(request: bytes) -> str:
		""" Login the peer to the directory

		Parameters:
			request - the list containing the request parameters

		Returns:
			str - the response
		"""
		if request.__len__() != 66:
			return "Invalid request. Usage is: LOGI.<your_ip>.<your_port>"

		ip = request[5:60].decode('UTF-8')
		port = request[61:66].decode('UTF-8')

		peer = Peer(str(uuid.uuid4().hex[:16].upper()), ip, port)
		peer.insert()

		return "ALGI."+peer.session_id

	@staticmethod
	def logout(request: bytes) -> str:
		""" Logout the peer from the directory

		Parameters:
			request - the list containing the request parameters

		Returns:
			str - the response
		"""
		if request.__len__() != 21:
			return "Invalid request. Usage is: LOGO.<your_session_id>"

		session_id = request[5:21].decode('UTF-8')

		peer = Peer.get_first(session_id)

		deleted = peer.delete()

		return "ALGO."+str(deleted)

	@staticmethod
	def add_file(request: bytes) -> str:
		""" Add a file to the directory

		Parameters:
			request - the list containing the request parameters

		Returns:
			str - the response
		"""
		if request.__len__() != 155:
			return "Invalid request. Usage is: ADDF.<your_session_id>.<file_md5>.<filename>"

		session_id = request[5:21].decode('UTF-8')
		md5 = request[22:54].decode('UTF-8')
		name = request[55:155].decode('UTF-8')

		# conn = database.get_connection()

		return "This is the response for ADDF"

	@staticmethod
	def delete_file(request: bytes) -> str:
		""" Delete a file from the directory
		
		Parameters:
			request - the list containing the request parameters

		Returns:
			str - the response
		"""
		if request.__len__() != 54:
			return "Invalid request. Usage is: DELF.<your_session_id>.<file_md5>"

		session_id = request[5:21].decode('UTF-8')
		md5 = request[22:54].decode('UTF-8')

		# conn = database.get_connection()

		return "This is the response for DELF"

	@staticmethod
	def find_file(request: bytes) -> str:
		""" Find a file in the directory
		
		Parameters:
			request - the list containing the request parameters

		Returns:
			str - the response
		"""
		if request.__len__() != 42:
			return "Invalid command. Usage is: FIND.<your_session_id>.<query_string>"

		session_id = request[5:21].decode('UTF-8')
		query = request[22:42].decode('UTF-8')

		# conn = database.get_connection()

		return "This is the response for FIND"

	@staticmethod
	def register_download(request: bytes) -> str:
		""" Register a file download

		
		Parameters:
			request - the list containing the request parameters

		Returns:
			str - the response
		"""
		if request.__len__() != 54:
			return "Invalid request. Usage is: DREG.<your_session_id>.<file_md5>"

		session_id = request[5:21].decode('UTF-8')
		md5 = request[22:54].decode('UTF-8')

		# conn = database.get_connection()

		return "This is the response for DREG"
