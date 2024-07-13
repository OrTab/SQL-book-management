from flask import Blueprint, render_template, send_from_directory, redirect
from services.books_service import get_books_from_db

bp = Blueprint("index", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/books")
def get_books_page():
    # if not authenticated
    if False:
        return redirect("/login", 307)
    try:
        books = get_books_from_db()
        return render_template("books.html", books=books)
    except Exception as error:
        print(error)
        return redirect("/", 307)


@bp.route("/login")
def get_login_page():
    return render_template("login.html")


@bp.route("/signup")
def get_signup_page():
    return render_template("signup.html")


@bp.route("/<path:filename>")
def serve_file(filename):
    return send_from_directory("static", filename)
