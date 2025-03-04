import mysql.connector
import creds
from mysql.connector import Error

mycreds = creds.Creds()
conString = mycreds.conString
username = mycreds.userName
password = mycreds.password
dbName = mycreds.dbName

def create_conn():
    connection = None
    try:
        mysql.connector.connect(
            host = conString,
            user = username,
            passwd = password,
            database = dbName
        )
        print("Connection successful")
        return connection
    except Error as e:
        print(f'An error {e} occured', e)
        return None

create_conn()
    
        
