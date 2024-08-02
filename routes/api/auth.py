from flask import Blueprint

bp = Blueprint("api", __name__)
from config import login_token_cookie_name
from flask import Blueprint, request, redirect, flash, render_template, url_for
from services.db_service import db_operation
from error_entities.database_duplication_entry_error import DatabaseDuplicationEntryError
from error_entities.database_operation_error import DatabaseOperationError
from error_entities.incorrect_username_password_error import IncorrectUsernamePassword
from error_entities.empty_username_password_error import EmptyUsernamePassword
from services.users_service import (
    encrypt_decrypt_password,
    validate_username_password_existence,is_authenticated
)


@bp.route("/login", methods=["POST"])
def login():
    try:
        if(is_authenticated()):
            return { "message" :"already logged in" } 

        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        validate_username_password_existence(username, password)

        query = "SELECT * FROM users WHERE username = %s"
        user_response = db_operation(query, (username,))
        user = user_response[0] if user_response else None
        if not user:
            raise IncorrectUsernamePassword()

        decrypted_password = encrypt_decrypt_password(user["password"])
        if decrypted_password != password:
            raise IncorrectUsernamePassword()

        query = """INSERT INTO tokens (id, token, user_id, expiration)
                    VALUES (UUID(), UUID(), %s, DATE_ADD(NOW(), INTERVAL 1 MONTH))
                """
        db_operation(query, (user["id"],))
        query = """
            SELECT id, token, expiration
            FROM tokens
            WHERE user_id = %s
        """
        token_response = db_operation(query, (user["id"],), True)
        flash(f"Hey {user["username"]}, welcome back", category="message")
        response = redirect("/books")
        response.set_cookie(
            login_token_cookie_name,
            token_response["token"],
            expires=token_response["expiration"],
            httponly=True,
        )
        return response

    except (IncorrectUsernamePassword , EmptyUsernamePassword)as error:
        flash(str(error), category="error")
        return redirect(url_for("index.login", username=username))
    except (DatabaseDuplicationEntryError, Exception) as error:
        flash("An error occurred. Please try again later.", category="error")
        if isinstance(error, DatabaseDuplicationEntryError):
            print(f"Should handle deletion of token row and create new, error: {error}")
        return redirect(url_for('index.login', username=username))


@bp.route("/signup", methods=["POST"])
def create_user():
    try:
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        validate_username_password_existence(username, password)
        password = encrypt_decrypt_password(password)
        user_data = (username, password)
        query = "INSERT INTO users (id, username, password, created_at) VALUES (UUID(), %s, %s, CURRENT_TIMESTAMP)"
        db_operation(query, user_data)
        flash("user created successfully", category="success")
        flash(f"Hey {username}, welcome back", category="message")
        return redirect("/books")
    except EmptyUsernamePassword as error:
        flash(str(error), category="error")
        return redirect(url_for("index.signup"))
    except DatabaseDuplicationEntryError as error:
        flash("Username or email already exists. Please login.", category="message")
        return redirect(url_for("index.login", username=username))
    except DatabaseOperationError as error:
        flash("An unexpected error occurred. Please try again later.", category="error")
        return render_template("signup.html")
