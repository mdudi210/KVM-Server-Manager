import mysql.connector
from mysql.connector.errors import get_exception , get_mysql_exception , DatabaseError

class OpenDb:
    # ,query,query_argument,fetch_type=''
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "Watchguard@01"
        self.database = "kvmserver"

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


