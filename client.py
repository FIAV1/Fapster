#!/usr/bin/env python

import socket
import sys

server = input('Server: ')
version = int(input('Version: '))

while True:

	data = input('Messaggio: ')

	if version == 4:
		sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	elif version == 6:
		sd = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
	else:
		print('Puoi scegliere solo 4 o 6')
		break

	try:
		sd.connect((server, 3000))
		print('Connessione avvenuta\n')
	except OSError as e:
		print(f'Errore sulla socket: {e}')
		sys.exit(0)

	with sd:
		sd.sendall(bytes(data, 'UTF-8'))
		data = sd.recv(1024)
		response = data.decode('UTF-8')
		print(f'Ricevuto: {data}')
		sd.close()
