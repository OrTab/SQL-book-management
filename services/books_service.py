from services.db_service import db_operation


def get_books_from_db():
    query = "SELECT * FROM books"
    response = db_operation(query)
    return response
