from flask import Blueprint
from services.books_service import get_books_from_db

bp = Blueprint("books", __name__)


@bp.before_request
def authenticate_user():
    return None


@bp.route("/")
def get_books():
    return get_books_from_db()
