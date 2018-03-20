#!/usr/bin/env python

from database import database
from model.Peer import Peer
from model.File import File
from model import peer_repository
from model import file_repository
import uuid


db_file = 'directory.db'


def serve(request: bytes) -> str:
	""" Handle the peer request
	Parameters:
		request - the list containing the request parameters
	Returns:
		str - the response
	"""
	command = request[0:4].decode('UTF-8')

	if command == "LOGI":

		if len(request) != 64:
			return "0" * 16

		ip = request[4:59].decode('UTF-8')
		port = request[59:64].decode('UTF-8')

		try:
			conn = database.get_connection(db_file)
			conn.row_factory = database.sqlite3.Row

		except database.Error as e:
			print(f'Error: {e}')
			return "0" * 16

		try:
			peer = peer_repository.find_by_ip(conn, ip)

			# if the peer didn't already logged in
			if peer is None:
				session_id = str(uuid.uuid4().hex[:16].upper())
				peer = peer_repository.find(conn, session_id)

				# while the generated session_id exists
				while peer is not None:
					session_id = str(uuid.uuid4().hex[:16].upper())
					peer = peer_repository.find(conn, session_id)

				peer = Peer(session_id, ip, port)
				peer.insert(conn)

			conn.commit()
			conn.close()

		except database.Error as e:
			conn.close()
			print(f'Error: {e}')
			return "0" * 16

		return "ALGI" + peer.session_id

	elif command == "ADDF":

		if len(request) != 152:
			return "Invalid request. Usage is: ADDF<your_session_id><file_md5><filename>"

		session_id = request[4:20].decode('UTF-8')
		md5 = request[20:52].decode('UTF-8')
		name = request[52:152].decode('UTF-8').lower()

		try:
			conn = database.get_connection(db_file)
			conn.row_factory = database.sqlite3.Row

		except database.Error as e:
			print(f'Error: {e}')
			return "The server has encountered an error while trying to serve the request."

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

			num_copies = file_repository.get_copies(conn, md5)

			conn.commit()
			conn.close()

		except database.Error as e:
			conn.rollback()
			conn.close()
			print(f'Error: {e}')
			return "The server has encountered an error while trying to serve the request."

		return "AADD" + str(num_copies).zfill(3)

	elif command == "DELF":

		if len(request) != 52:
			return "Invalid request. Usage is: DELF<your_session_id><file_md5>"

		session_id = request[4:20].decode('UTF-8')
		md5 = request[20:52].decode('UTF-8')

		try:
			conn = database.get_connection(db_file)
			conn.row_factory = database.sqlite3.Row

		except database.Error as e:
			print(f'Error: {e}')
			return "The server has encountered an error while trying to serve the request."

		try:
			peer = peer_repository.find(conn, session_id)

			if peer is None:
				conn.close()
				return "Unauthorized: your SessionID is invalid"

			if not file_repository.peer_has_file(conn, session_id, md5):
				conn.close()
				return "ADEL999"

			peer_repository.file_unlink(conn, session_id, md5)

			copy = file_repository.get_copies(conn, md5)

			if copy == 0:
				file = file_repository.find(conn, md5)
				file.delete(conn)

			conn.commit()
			conn.close()

		except database.Error as e:
			conn.rollback()
			conn.close()
			print(f'Error: {e}')
			return "The server has encountered an error while trying to serve the request."

		return "ADEL" + str(copy).zfill(3)

	elif command == "FIND":

		if len(request) != 40:
			return "Invalid command. Usage is: FIND<your_session_id><query_string>"

		session_id = request[4:20].decode('UTF-8')
		query = request[20:40].decode('UTF-8').lower().lstrip().rstrip()

		if query != '*':
			query = '%' + query + '%'

		try:
			conn = database.get_connection(db_file)
			conn.row_factory = database.sqlite3.Row

		except database.Error as e:
			print(f'Error: {e}')
			return "The server has encountered an error while trying to serve the request."

		try:
			peer = peer_repository.find(conn, session_id)

			if peer is None:
				conn.close()
				return "Unauthorized: your SessionID is invalid"

			total_file = file_repository.get_files_count_by_querystring(conn, query)
			if total_file == 0:
				return 'AFIN' + str(total_file).zfill(3)

			result = str(total_file).zfill(3)

			file_list = file_repository.get_files_with_copy_amount_by_querystring(conn, query)

			for file_row in file_list:
				file_md5 = file_row['file_md5']
				file_name = file_row['file_name']
				copies = file_row['copies']

				result = result + file_md5 + file_name + str(copies).zfill(3)

				peer_list = peer_repository.get_peers_by_file(conn, file_md5)

				for peer_row in peer_list:
					peer_ip = peer_row['ip']
					peer_port = peer_row['port']

					result = result + peer_ip + peer_port

			conn.commit()
			conn.close()

		except database.Error as e:
			conn.rollback()
			conn.close()
			print(f'Error: {e}')
			return "The server has encountered an error while trying to serve the request."

		return "AFIN" + result

	elif command == "DREG":

		if len(request) != 52:
			return "Invalid request. Usage is: DREG<your_session_id><file_md5>"

		session_id = request[4:20].decode('UTF-8')
		md5 = request[20:52].decode('UTF-8')

		try:
			conn = database.get_connection(db_file)
			conn.row_factory = database.sqlite3.Row

		except database.Error as e:
			print(f'Error: {e}')
			return "The server has encountered an error while trying to serve the request."

		try:
			peer = peer_repository.find(conn, session_id)

			if peer is None:
				conn.close()
				return "Unauthorized: your SessionID is invalid"

			file = file_repository.find(conn, md5)

			if file is None:
				return "File not found."

			file.download_count += 1
			file.update(conn)

			conn.commit()
			conn.close()

		except database.Error as e:
			conn.rollback()
			conn.close()
			print(f'Error: {e}')
			return "The server has encountered an error while trying to serve the request."

		return "ADRE" + str(file.download_count).zfill(5)

	elif command == "LOGO":

		if len(request) != 20:
			return "Invalid request. Usage is: LOGO<your_session_id>"

		session_id = request[4:20].decode('UTF-8')

		try:
			conn = database.get_connection(db_file)
			conn.row_factory = database.sqlite3.Row

		except database.Error as e:
			print(f'Error: {e}')
			return "The server has encountered an error while trying to serve the request."

		try:
			peer = peer_repository.find(conn, session_id)

			if peer is None:
				conn.close()
				return "Unauthorized: your SessionID is invalid"

			deleted = file_repository.delete_peer_files(conn, session_id)

			peer.delete(conn)

			conn.commit()
			conn.close()

		except database.Error as e:
			conn.rollback()
			conn.close()
			print(f'Error: {e}')
			return "The server has encountered an error while trying to serve the request."

		return "ALGO" + str(deleted).zfill(3)

	else:
		return "Command \'" + request.decode('UTF-8') + "\' is invalid, try again."
