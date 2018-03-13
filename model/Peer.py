#!/usr/bin/env python

from database import database


class Peer:

    def __init__(self, session_id, ip, port):
        self.session_id = session_id
        self.ip = ip
        self.port = port

    def insert(self, conn: database.sqlite3.Connection) -> None:
        """ Insert a peer into db

        Parameters:
            conn - the db connection
        Returns:
            bool - true or false either if it succeed or it fails
        """
        conn.execute('INSERT INTO peers VALUES (?,?,?)', (self.session_id, self.ip, self.port))

    def delete(self, conn: database.sqlite3.Connection) -> int:
        """ Delete a peer from db

        Parameters:
            conn - the db connection
        Returns:
            int - number of file deleted, owned by the peer
        """
        deleted = conn.execute('SELECT * FROM peers NATURAL JOIN files_peers WHERE session_id=?', (self.session_id,)).rowcount
        conn.execute('DELETE FROM peers WHERE session_id = ?', (self.session_id,))
        
        return deleted
