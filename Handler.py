#!/usr/bin/env python

from Controller import Controller


class Handler:

	@staticmethod
	def serve(request: str) -> str:
		""" Handle the peer request and call the right Controller method
		:param: request: the string containing the request
		:return: str: the string containinf the response
		"""
		parameters = request.split(".")
		del request
		command = parameters[0]

		if command == "LOGI":
			return Controller.login(parameters)
		elif command == "ADDF":
			return Controller.add_file(parameters)
		elif command == "DELF":
			return Controller.delete_file(parameters)
		elif command == "FIND":
			return Controller.find_file(parameters)
		elif command == "DREG":
			return Controller.register_download(parameters)
		elif command == "LOGO":
			return Controller.logout(parameters)
		else:
			return "Command \'" + command + "\' is invalid, try again."
