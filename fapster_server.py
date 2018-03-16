#!/usr/bin/env python

from service.Server import Server
from database import database
from utils import shell_colors as shell

if __name__ == '__main__':

	shell.print_yellow('__________                     _____')
	shell.print_yellow('___  ____/_____ _________________  /_____________')
	shell.print_yellow('__  /_   _  __ `/__  __ \_  ___/  __/  _ \_  ___/')
	shell.print_yellow('_  __/   / /_/ /__  /_/ /(__  )/ /_ /  __/  / ')
	shell.print_yellow('/_/      \__,_/ _  .___//____/ \__/ \___//_/')
	shell.print_yellow('                /_/')

	DB_FILE = 'directory.db'

	if not database.exist(DB_FILE):
		database.create_database(DB_FILE)
	else:
		database.reset_database(DB_FILE)

	Server(3000).run()
