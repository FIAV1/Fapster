#!/usr/bin/env python

from database import database
from model.Peer import Peer
from model import peer_repository
import uuid


def serve(request: bytes) -> str:
	""" Handle the peer request
	Parameters:
		request - the list containing the request parameters
	Returns:
		str - the response
	"""
	command = request[0:4].decode('UTF-8')

	if command == "LOGI":
		if request.__len__() != 64:
			return "Invalid request. Usage is: LOGI.<your_ip>.<your_port>"

		ip = request[4:59].decode('UTF-8')
		port = request[60:64].decode('UTF-8')
		peer = Peer(str(uuid.uuid4().hex[:16].upper()), ip, port)
		conn = database.get_connection()

		try:
			peer.insert(conn)
			conn.commit()
			conn.close()

		except database.Error as e:
			conn.rollback()
			conn.close()
			print(f'Error: {e}')
			return "The server has encountered an error while trying to serve the request."

		return "ALGI" + peer.session_id

	elif command == "ADDF":
		if request.__len__() != 155:
			return "Invalid request. Usage is: ADDF.<your_session_id>.<file_md5>.<filename>"

		session_id = request[5:21].decode('UTF-8')
		md5 = request[22:54].decode('UTF-8')
		name = request[55:155].decode('UTF-8')

		conn = database.get_connection()
		conn.close()

		return "This is the response for ADDF"

	elif command == "DELF":
		if request.__len__() != 54:
			return "Invalid request. Usage is: DELF.<your_session_id>.<file_md5>"

		session_id = request[5:21].decode('UTF-8')
		md5 = request[22:54].decode('UTF-8')

		conn = database.get_connection()
		conn.close()

		return "This is the response for DELF"

	elif command == "FIND":
		if request.__len__() != 42:
			return "Invalid command. Usage is: FIND.<your_session_id>.<query_string>"

		session_id = request[5:21].decode('UTF-8')
		query = request[22:42].decode('UTF-8')

		conn = database.get_connection()
		conn.close()

		return "This is the response for FIND"

	elif command == "DREG":
		if request.__len__() != 54:
			return "Invalid request. Usage is: DREG.<your_session_id>.<file_md5>"

		session_id = request[5:21].decode('UTF-8')
		md5 = request[22:54].decode('UTF-8')

		conn = database.get_connection()
		conn.close()

		return "This is the response for DREG"

	elif command == "LOGO":
		if request.__len__() != 20:
			return "Invalid request. Usage is: LOGO.<your_session_id>"

		session_id = request[4:20].decode('UTF-8')
		conn = database.get_connection()

		try:
			peer = peer_repository.find(conn, session_id)
			deleted = peer.delete(conn)
			conn.commit()
			conn.close()

		except database.Error as e:
			conn.rollback()
			conn.close()
			print(f'Error: {e}')
			return "The server has encountered an error while trying to serve the request."

		return "ALGO"+str(deleted)

	else:
		return "Command \'" + request.decode('UTF-8') + "\' is invalid, try again."
