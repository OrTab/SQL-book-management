import mysql.connector
from config import db_name, password, host, user
from error_entities.database_operation_error import DatabaseOperationError
from error_entities.database_duplication_entry_error import (
    DatabaseDuplicationEntryError,
)


mysql_error_mapping = {
    mysql.connector.errorcode.ER_DUP_ENTRY: DatabaseDuplicationEntryError
}


class MySQLConnection:
    def __init__(self):
        self.db_connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.db_connection = mysql.connector.connect(
                user=user, database=db_name, password=password, host=host
            )
            self.cursor = self.db_connection.cursor(dictionary=True)
            print(f"Database {db_name} connected successfully")
            return {"cursor": self.cursor, "db_connection": self.db_connection}
        except mysql.connector.Error as error:
            return error.msg

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()


def db_operation(query, params=None):
    try:
        with MySQLConnection() as config:
            if isinstance(config, str):
                raise Exception(config)

            cursor = config["cursor"]
            db_connection = config["db_connection"]
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if query.strip().startswith(("INSERT", "UPDATE", "DELETE")):
                db_connection.commit()

            if query.strip().startswith("SELECT"):
                results = cursor.fetchall()
                return results
    except mysql.connector.Error as error:
        error_message = f"MySQL Error: {error.msg}"
        error_type_entity = mysql_error_mapping.get(error.errno, DatabaseOperationError)
        raise error_type_entity(error_message)
    except Exception as error:
        error_message = f"Error running operation on database: {str(error)}"
        raise DatabaseOperationError(error_message, 500)
