#!/usr/bin/env python

from database import database
from model.Peer import Peer
from model.File import File
from model import peer_repository
from model import file_repository
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
		port = request[59:64].decode('UTF-8')
		peer = Peer(str(uuid.uuid4().hex[:16].upper()), ip, port)

		conn = database.get_connection('directory.db')

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
		if request.__len__() != 152:
			return "Invalid request. Usage is: ADDF.<your_session_id>.<file_md5>.<filename>"

		session_id = request[4:20].decode('UTF-8')
		md5 = request[20:52].decode('UTF-8')
		name = request[52:152].decode('UTF-8')

		conn = database.get_connection('directory.db')
		conn.row_factory = database.sqlite3.Row

		try:
			peer = peer_repository.find(conn, session_id)

			if peer is None:
				conn.close()
				return "Unauthorized: your SessionID is invalid"

			file = file_repository.find(conn, md5)

			if file is None:
				file = File(md5, name, 0)
				file.insert(conn)
				file_repository.add_owner(conn, md5, session_id)
			else:
				file.file_name = name
				file.update(conn)
				if not file_repository.peer_has_file(conn, session_id, md5):
					file_repository.add_owner(conn, md5, session_id)

			conn.commit()

			num_copies = file_repository.get_copies(conn, md5)
			conn.close()
		except database.Error as e:
			conn.rollback()
			conn.close()
			print(f'Error: {e}')
			return "The server has encountered an error while trying to serve the request."

		return "AADD" + str(num_copies)

	elif command == "DELF":
		if request.__len__() != 54:
			return "Invalid request. Usage is: DELF.<your_session_id>.<file_md5>"

		session_id = request[5:21].decode('UTF-8')
		md5 = request[22:54].decode('UTF-8')

		conn = database.get_connection('directory.db')
		conn.close()

		return "This is the response for DELF"

	elif command == "FIND":
		if request.__len__() != 40:
			return "Invalid command. Usage is: FIND.<your_session_id>.<query_string>"

		session_id = request[4:20].decode('UTF-8')
		query = request[20:40].decode('UTF-8')

		conn = database.get_connection('directory.db')
		conn.row_factory = database.sqlite3.Row

		try:
			peer = peer_repository.find(conn, session_id)

			if peer is None:
				conn.close()
				return "Unauthorized: your SessionID is invalid"

			resultset = file_repository.search(conn, query)

			conn.close()
		except database.Error as e:
			conn.rollback()
			conn.close()
			print(f'Error: {e}')
			return "The server has encountered an error while trying to serve the request."

		return "AFIN" + resultset

	elif command == "DREG":
		if request.__len__() != 54:
			return "Invalid request. Usage is: DREG.<your_session_id>.<file_md5>"

		session_id = request[5:21].decode('UTF-8')
		md5 = request[22:54].decode('UTF-8')

		conn = database.get_connection('directory.db')
		conn.close()

		return "This is the response for DREG"

	elif command == "LOGO":
		if request.__len__() != 20:
			return "Invalid request. Usage is: LOGO.<your_session_id>"

		session_id = request[4:20].decode('UTF-8')
		conn = database.get_connection('directory.db')
		conn.row_factory = database.sqlite3.Row

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
