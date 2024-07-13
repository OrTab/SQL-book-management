import mysql.connector
from config import db_name, password, host, user

mysql_connector = mysql.connector


class DatabaseOperationError(Exception):
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.type = "db_operation_error"
        self.message = message
        self.status_code = status_code


class MySQLConnection:
    def __enter__(self):
        global mysql_connector
        try:
            self.db = mysql_connector.connect(
                user=user, database=db_name, password=password, host=host
            )
            self.cursor = self.db.cursor(dictionary=True)
            print(f"Database {db_name} connected successfully")
            return {"cursor": self.cursor, "db": self.db}
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


def db_operation(query, operation_config, params=None):
    try:
        with MySQLConnection() as config:
            cursor = config["cursor"]
            db = config["db"]
            print(operation_config)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if operation_config.get("should_fetch"):
                response = cursor.fetchall()
                return response

            if operation_config.get("should_commit"):
                db.commit()

    except mysql_connector.Error as error:
        error_message = f"MySQL Error: {error.msg}"
        raise DatabaseOperationError(error_message, 500)
    except Exception as error:
        error_message = f"Error running operation on database: {str(error)}"
        raise DatabaseOperationError(error_message, 500)
