#!/usr/bin/env python

from ..database import database

def authenticate(ipClient, portClient):
    """ Authenticate a client, storing its ip and port and generating a random unique session_id
        :param ipClient: Client ip address
        :param portClient: Client port number
        :return: Boolean
    """
    query = """ SELECT * FROM peers
                WHERE ip = """+ipClient
            
    conn = database.createConnection("directory.db")
    authenticated = database.execQuery(conn, query)

    print(authenticated)
