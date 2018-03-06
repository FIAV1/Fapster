#!/usr/bin/env python

import socket
import sys
import os

PORT = 3000


def child():
	(client, client_port) = socket.getnameinfo(clientaddr, socket.NI_NUMERICHOST)
	print(f'Client {client} on port {client_port}. Child PID: {os.getpid()}\n')
	ss.close()
	while True:
		data = sd.recv(1024)
		print(f'Received: {data}')
		if not data:
			sd.close()
			break
		sd.send(data)
	os._exit(0)


# The server will listen to the first address family available.
# On most of IPv6-ready systems, IPv6 will take precedence and the server may not accept IPv4 traffic.
for res in socket.getaddrinfo(None, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):

	(family, type, proto, canonname, sockaddr) = res

	try:
		# Create the socket
		ss = socket.socket(family, type, proto)
	except OSError:
		ss = None
		continue
	try:
		# Set the SO_REUSEADDR flag in order to tell the kernel to reuse the socket even if it's in a TIME_WAIT state,
		# without waiting for its natural timeout to expire.
		# This is because sockets in a TIME_WAIT state can’t be immediately reused.
		ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		# Bind the local address (sockaddr) to the socket (ss)
		ss.bind(sockaddr)

		# Transform the socket in a passive socket and
		# define a queue of SOMAXCONN possible connection requests
		ss.listen(socket.SOMAXCONN)
	except OSError:
		ss = None
		continue

	break

if ss is None:
	print('Could not open socket')
	sys.exit(socket.error)

print(f'Server {sockaddr[0]} listening on port {sockaddr[1]}...')

while True:
	# Put the passive socket on hold for connection requests
	(sd, clientaddr) = ss.accept()

	pid = os.fork()
	if pid == 0:  # --------FIGLIO-------
		child()
	# ----------------------------------

	sd.close()
