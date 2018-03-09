#!/usr/bin/env python

# import database.database as database


class Controller:

	@staticmethod
	def login(parameters: list) -> str:
		""" Login the peer to the directory
		:param: request: the list containing the request parameters
		:return: str: the response
		"""
		# conn = database.get_connection()

		return "This is the response for LOGI"

	@staticmethod
	def logout(parameters: list) -> str:
		""" Logout the peer from the directory
		:param: request: the list containing the request parameters
		:return: str: the response
		"""
		# conn = database.get_connection()

		return "This is the response for LOGO"

	@staticmethod
	def add_file(parameters: list) -> str:
		""" Add a file to the directory
		:param: request: the list containing the request parameters
		:return: str: the response
		"""
		# conn = database.get_connection()

		return "This is the response for ADDF"

	@staticmethod
	def delete_file(parameters: list) -> str:
		""" Delete a file from the directory
		:param: request: the list containing the request parameters
		:return: str: the response
		"""
		# conn = database.get_connection()

		return "This is the response for DELF"

	@staticmethod
	def find_file(parameters: list) -> str:
		""" Find a file in the directory
		:param: request: the list containing the request parameters
		:return: str: the response
		"""
		# conn = database.get_connection()

		return "This is the response for FIND"

	@staticmethod
	def register_download(parameters: list) -> str:
		""" Register a file download
		:param: request: the list containing the request parameters
		:return: str: the response
		"""
		# conn = database.get_connection()

		return "This is the response for DREG"
