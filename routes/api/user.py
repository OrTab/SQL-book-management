from flask import Blueprint, request
from services.db_service import db_operation
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
        query = "SELECT COUNT(*) AS user_count FROM users WHERE username = %s AND password = %s"
        response = db_operation(query, {"should_fetch": True}, user_data)
        user_count = response[0]["user_count"]
        if user_count == 0:
            query = "INSERT INTO users (id, username, password, created_at) VALUES (UUID(), %s, %s, CURRENT_TIMESTAMP)"
            db_operation(query, {"should_commit": True}, user_data)
            print("user created successfully")
        else:
            print("user exist lets return login page with message")
    except Exception as error:
        print(error)

    return user_data
