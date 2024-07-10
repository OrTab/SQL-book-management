from flask import Blueprint
from services.books_service import get_books_from_db, DatabaseOperationError

bp = Blueprint("books", __name__)


@bp.before_request
def authenticate_user():
    return None


@bp.route("/")
def get_books():
    try:
        return get_books_from_db()
    except DatabaseOperationError as error:
        return {"error": "Something went wrong"}, error.status_code
