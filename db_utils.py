import mysql.connector
from config import USER, PASSWORD, HOST, DATABASE

class DbConnectionError(Exception):
    pass
# Establish a connection to the database using provided credentials
def _connect_to_db():
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    return cnx