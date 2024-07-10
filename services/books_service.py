from services.db_service import db_operation, DatabaseOperationError


def get_books_from_db():
    try:
        query = "SELECT * FROM books"
        response = db_operation(query)
    except Exception as error:
        raise error
