from flask import Blueprint
from services.books_service import get_books_from_db, DatabaseOperationError
from services.users_service import requires_authentication

bp = Blueprint("books", __name__)


@bp.route("/")
@requires_authentication
def get_books():
    try:
        books = get_books_from_db()
        return books
    except DatabaseOperationError as error:
        return {"error": "Something went wrong"}, error.status_code
