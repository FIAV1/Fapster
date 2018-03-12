#!/usr/bin/env python

import socket
import sys
import os
import selectors

PORT = 3000
sel = selectors.DefaultSelector()


def child():
	(client, client_port) = socket.getnameinfo(clientaddr, socket.NI_NUMERICHOST)
	print(f'Client {client} on port {client_port}. Child PID: {os.getpid()}.\n')
	ss4.close()
	ss6.close()
	while True:
		data = sd.recv(1024)
		print(f'Received: {data}')
		if not data:
			sd.close()
			break
		sd.send(data)
	os._exit(0)


try:
	# Create the sockets
	ss4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ss6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
except OSError:
	print(f'Can\'t create the sockets: {OSError}')
	sys.exit(socket.error)

try:
	# Set the SO_REUSEADDR flag in order to tell the kernel to reuse the socket even if it's in a TIME_WAIT state,
	# without waiting for its natural timeout to expire.
	# This is because sockets in a TIME_WAIT state can’t be immediately reused.
	ss4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	ss6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# Bind the local address to the sockets (ss4, ss6)
	ss4.bind(('', PORT))
	ss6.bind(('', PORT))

	# Transform the socket in a passive socket and
	# define a queue of SOMAXCONN possible connection requests
	ss4.listen(socket.SOMAXCONN)
	ss6.listen(socket.SOMAXCONN)

	# Set the sockets to be non-blocking in order to have
	# a non-blocking accept()
	ss4.setblocking(False)
	ss6.setblocking(False)
except OSError:
	print(f'Can\'t handle the sockets: {OSError}')
	sys.exit(socket.error)

# Register the socket ss4 for selection, monitoring it for Input events.
sel.register(ss4, selectors.EVENT_READ)
# Register the socket ss6 for selection, monitoring it for Input events.
sel.register(ss6, selectors.EVENT_READ)

print('Server listening...')

while True:
	# Wait until some registered file objects become ready, or the timeout expires
	# This returns a list of (key, events) tuples, one for each ready file object
	#
	# We use the select in order to wait incoming connections on both the sockets simultaneously:
	# once the passive socket has a connection ready (the client has called the connect())
	# the select "is triggered" and the accept will be non-blocking
	events = sel.select()

	for (key, mask) in events:
		# • key is the SelectorKey instance corresponding to a ready file object
		# A SelectorKey is a namedtuple used to associate a file object to its underlying
		# file descriptor, selected event mask and attached data
		# • mask is a bitmask of events ready on this file object.
		sock = key.fileobj

		# Put the passive socket on hold for connection requests
		(sd, clientaddr) = sock.accept()

		# Explicitly set with the desired socket options.(Best practice)
		sd.setblocking(True)

		pid = os.fork()
		if pid == 0:  # --------FIGLIO-------
			child()
		# ----------------------------------

		sd.close()
