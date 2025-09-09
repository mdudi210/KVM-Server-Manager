import mysql.connector
from mysql.connector.errors import get_exception , get_mysql_exception , DatabaseError
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

class OpenDb:
    def __init__(self):
        self.host = DB_HOST
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.database = DB_DATABASE

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            return self.connection.cursor()
        except DatabaseError as e:
            print("This is sql error : "+e.msg)
        except AttributeError:
            print("This is sql error : ")

        

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.connection.commit()
            self.connection.close()
        except DatabaseError as e:
            print("This is sql error : "+e.msg)
        except AttributeError as e:
            print("This is sql error : ")


