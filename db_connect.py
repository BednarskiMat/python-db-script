import mysql.connector
from mysql.connector import Error

class Connection:
    
    def __init__(self, host_name, user_name, user_password) -> None:
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password

        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=self.host_name,
                user=self.user_name,
                passwd=self.user_password
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
    
    def return_connection(self):
        return self.connection

    def create_database(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Database created successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
            return True
        except Error as e:
            print(f"The error '{e}' occurred")
            return False