#!/usr/bin/env python

import database.database as database

class Peer:

    def __init__(self, session_id, ip, port):
        self.session_id = session_id
        self.ip = ip
        self.port = port
    
    def insert(self):
        """ Insert a Peer in db
        """

        conn = database.createConnection("directory.db")

        query = """ INSERT INTO peers (
                session_id,
                ip,
                port) VALUES (
                    'adf123qwe567',
                    '192.168.1.1',
                    '3000'
                ) """
        database.execQuery(conn, query)

        conn.commit()
