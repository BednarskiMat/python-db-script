from mimetypes import init
import os, sys, json 
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import connection

sys.path.append(".")
from connection import Connection

load_dotenv() # get db info from root 
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
environments ={
    #Name/key: host 
    "DEV": os.getenv("local_db_host")
}



        
def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

connection = create_connection(environments["DEV"], db_user, db_password)
connection = Connection('127.0.0.1', db_user, db_password).return_connection()
select_users = "show databases"
users = execute_read_query(connection, select_users)
print(users)
