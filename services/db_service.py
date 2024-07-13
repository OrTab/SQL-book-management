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
    def __enter__(self):
        try:
            self.db = mysql.connector.connect(
                user=user, database=db_name, password=password, host=host
            )
            self.cursor = self.db.cursor(dictionary=True)
            print(f"Database {db_name} connected successfully")
            return {"cursor": self.cursor, "db": self.db}
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.db and self.db.is_connected():
            self.db.close()


def db_operation(query, params=None):
    try:
        with MySQLConnection() as config:
            cursor = config["cursor"]
            db = config["db"]
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if query.strip().startswith(("INSERT", "UPDATE", "DELETE")):
                cnx.commit()

            if query.strip().startswith("SELECT"):
                results = cursor.fetchall()
                return results

    except mysql.connector.Error as error:
        error_message = f"MySQL Error: {error.msg}"
        error_type_entity = mysql_error_mapping.get(error.errno, DatabaseOperationError)
        print("error_type_entity", error_type_entity)
        raise error_type_entity(error_message)
    except Exception as error:
        error_message = f"Error running operation on database: {str(error)}"
        raise DatabaseOperationError(error_message, 500)
