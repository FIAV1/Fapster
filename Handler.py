#!/usr/bin/env python

from Controller import Controller


class Handler:

	@staticmethod
	def serve(request: bytes) -> str:
		""" Handle the peer request and call the right Controller method
		:param: request: the string containing the request
		:return: str: the string containinf the response
		"""
		command = request[0:4].decode('UTF-8')

		if command == "LOGI":
			return Controller.login(request)
		elif command == "ADDF":
			return Controller.add_file(request)
		elif command == "DELF":
			return Controller.delete_file(request)
		elif command == "FIND":
			return Controller.find_file(request)
		elif command == "DREG":
			return Controller.register_download(request)
		elif command == "LOGO":
			return Controller.logout(request)
		else:
			return "Command \'" + request.decode('UTF-8') + "\' is invalid, try again."
