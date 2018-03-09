#!/usr/bin/env python

import database.database as database


class Peer:

    def __init__(self, session_id, ip, port):
        self.session_id = session_id
        self.ip = ip
        self.port = port
