from flask import Blueprint
from services.books_service import get_books_from_db

bp = Blueprint("books", __name__)


@bp.route("/")
def get_books():
    return get_books_from_db()
