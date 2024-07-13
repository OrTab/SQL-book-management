from flask import Blueprint, request, redirect, flash
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


@bp.route("/<user_id>")
def get_user(user_id):
    return {"answer": user_id}


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
        flash("user created successfully")
        return redirect("/signup")
    except DatabaseDuplicationEntryError:
        flash("Username or email already exists. Please login.")
        return redirect("/login")
    except DatabaseOperationError as error:
        if error.mysql_error_type == "duplicate_entry":
            flash("Username or email already exists. Please login.")
            return redirect("/login")
