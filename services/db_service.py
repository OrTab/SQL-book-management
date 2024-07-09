import mysql.connector
from config import db_name, password, host, user

mysql_connector = mysql.connector


class MySQLConnection:
    def __enter__(self):
        global mysql_connector
        try:
            self.db = mysql_connector.connect(
                user=user, database=db_name, password=password, host=host
            )
            self.cursor = self.db.cursor(dictionary=True)
            print(f"Database {db_name} connected successfully")
            return self.cursor
        except mysql_connector.Error as err:
            if err.errno == mysql_connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == mysql_connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.db and self.db.is_connected():
            self.db.close()


def db_operation(query, params={}):
    try:
        with MySQLConnection() as cursor:
            cursor.execute(query)
            response = cursor.fetchall()
            return response
    except mysql_connector.Error as error:
        error_message = f"MySQL Error: {error.msg}"
        return {"error": error_message}, 500
    except Exception as error:
        error_message = f"Error running operation on database: {str(error)}"
        return {"error": error_message}, 500
