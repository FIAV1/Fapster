#!/usr/bin/env python

from database.database import Database
from sqlite3 import Error


class Peer:

    def __init__(self, session_id, ip, port):
        self.session_id = session_id
        self.ip = ip
        self.port = port

    def get_first(session_id):
        """ Retrive first peer from database\n
        Parameters:
            session_id - session id for a peer
        Returns:
            peer - first matching result for the research
        """
        try:
            conn = Database().get_connection()

            try:
                c = conn.cursor()
                c.execute('SELECT * FROM peers WHERE session_id = ?', (session_id,))
                peer = c.fetchone()

            except Error as e:
                print(f'Errore: {e}')
                return None

            conn.commit()
            conn.close()

            return Peer(session_id, None, None)
        except Error as e:
            print(f'Errore: {e}')
            return None

    def insert(self):
        """ Insert a peer into db\n
        Parameters:
            self - model's parameters
        Returns:
            bool - true or false either if it succeed or it fails
        """
        try:
            conn = Database().get_connection()
            print(f'{conn}\n{Database().DB_FILE}')

            try:
                c = conn.cursor()
                c.execute('INSERT INTO peers VALUES (?,?,?)', (self.session_id, self.ip, self.port,))
                print(f'session id: {self.session_id}\nip: {self.ip}\nport: {self.port}')

            except Error as e:
                print(f'Errore: {e}')
                return False

            conn.commit()
            conn.close()

            return True
        except Error as e:
            print(f'Errore: {e}')
            return False

    def delete(self):
        """ Delete a peer from db\n
        Parameters:
            self - model's parameters
        Returns:
            int - number of file deleted, owned by the peer
        """
        try:
            conn = Database().get_connection()

            try:
                c = conn.cursor()
                c.execute('PRAGMA foreign_keys = ON')
                deleted = c.execute('DELETE FROM peers WHERE session_id = ?', (self.session_id,)).rowcount

            except Error as e:
                print(f'Errore: {e}')

                return False

            conn.commit()
            conn.close()

            return deleted

        except Error as e:
            print(f'Errore: {e}')
            return False
