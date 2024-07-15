from flask import Blueprint, render_template, send_from_directory, redirect, request
from services.books_service import get_books_from_db
from services.users_service import requires_authentication


bp = Blueprint("index", __name__)


@bp.route("/")
@requires_authentication
def index():
    return render_template("index.html")


@bp.route("/books")
@requires_authentication
def books():
    try:
        books = get_books_from_db()
        return render_template("books.html", books=books)
    except Exception as error:
        print(error)
        return redirect("/", 307)


@bp.route("/login")
def login():
    username = request.args.get("username")
    return render_template("login.html", username=username)


@bp.route("/signup")
def signup():
    return render_template("signup.html")


@bp.route("/<path:filename>")
def serve_file(filename):
    return send_from_directory("static", filename)
