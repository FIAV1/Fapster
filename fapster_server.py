#!/usr/bin/env python

from service.Server import Server
from database import database


if __name__ == '__main__':

	if not database.exist():
		database.create_database()
	else:
		database.refresh_databse()

	Server(3000).run()
