#!/usr/bin/env python

from service.Server import Server
from database import database


if __name__ == '__main__':

	if not database.exist('directory.db'):
		database.create_database('directory.db')
	else:
		database.reset_database('directory.db')

	Server(3000).run()
