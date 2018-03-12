#!/usr/bin/env python

import socket
import sys
import os
import multiprocessing
from Handler import Handler

PORT = 3000
BUFF_SIZE = 200


def child():
	(client, client_port) = socket.getnameinfo(clientaddr, socket.NI_NUMERICHOST)
	print(f'Client {client} on port {client_port}. Child PID: {os.getpid()}\n')
	ss.close()
	while True:
		request = sd.recv(BUFF_SIZE)
		response = Handler.serve(request)
		sd.sendall((bytes(response, 'UTF-8')))

		if response[0:4] == "ALGO":
			print(f'Client {client} on port {client_port} with PID: {os.getpid()} closed the connection.\n{response[5:]} files deleted.\n')
			break

	os._exit(0)


try:
	# Create the socket
	ss = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
except OSError as e:
	print(f'Can\'t create the socket: {e}')
	sys.exit(socket.error)

try:
	# Set the SO_REUSEADDR flag in order to tell the kernel to reuse the socket even if it's in a TIME_WAIT state,
	# without waiting for its natural timeout to expire.
	# This is because sockets in a TIME_WAIT state can’t be immediately reused.
	ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# Bind the local address (sockaddr) to the socket (ss)
	ss.bind(('', PORT))

	# Transform the socket in a passive socket and
	# define a queue of SOMAXCONN possible connection requests
	ss.listen(socket.SOMAXCONN)
except OSError:
	print(f'Can\'t handle the socket: {OSError}')
	sys.exit(socket.error)


print(f'Server {ss.getsockname()[0]} listening on port {ss.getsockname()[1]}...')

while True:
	# Put the passive socket on hold for connection requests
	(sd, clientaddr) = ss.accept()

	p = multiprocessing.Process(target=child)
	p.daemon = True
	p.start()

	sd.close()
