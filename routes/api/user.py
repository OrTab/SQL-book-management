from flask import Blueprint, request, redirect, flash, render_template
from services.db_service import (
    db_operation,
    DatabaseOperationError,
    DatabaseDuplicationEntryError,
)
from services.users_service import encrypt_decrypt_password

bp = Blueprint("user", __name__)


@bp.before_request
def authenticate_user():
    return None


@bp.route("/login", methods=["POST"])
def login():
    try:
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        if not username or not password:
            raise ValueError("Username or password cannot be empty.")

        query = "SELECT * FROM users WHERE username = %s"
        response = db_operation(query, (username,))
        user = response[0]
        if not user:
            raise ValueError("Incorrect username or password.")

        decrypted_password = encrypt_decrypt_password(user["password"])
        if decrypted_password != password:
            raise ValueError("Incorrect username or password.")

        flash(f"Hey {username}, welcome back", category="message")
        return redirect("/books")

    except ValueError as error:
        flash(str(error), category="error")
        return render_template("login.html")

    except Exception as error:
        flash("An error occurred. Please try again later.", category="error")
        print(f"Error during login: {error}")
        return render_template("login.html")


@bp.route("/signup", methods=["POST"])
def create_user():
    form_data = request.form
    username = form_data.get("username")
    password = form_data.get("password")
    password = encrypt_decrypt_password(password)
    user_data = (username, password)
    try:
        query = "INSERT INTO users (id, username, password, created_at) VALUES (UUID(), %s, %s, CURRENT_TIMESTAMP)"
        db_operation(query, user_data)
        flash("user created successfully", category="success")
        return redirect("/signup")
    except DatabaseDuplicationEntryError:
        flash("Username or email already exists. Please login.", category="message")
        return redirect("/login")
    except DatabaseOperationError as error:
        if error.mysql_error_type == "duplicate_entry":
            flash("Username or email already exists. Please login.")
            return redirect("/login")
