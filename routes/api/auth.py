from flask import Blueprint,session
from config import login_token_cookie_name
from flask import Blueprint, request, redirect, flash, render_template, url_for
from services.db_service import db_operation
from services.users_service import get_user_by_username
from error_entities.database_duplication_entry_error import DatabaseDuplicationEntryError
from error_entities.database_operation_error import DatabaseOperationError
from error_entities.incorrect_username_password_error import IncorrectUsernamePassword
from error_entities.empty_username_password_error import EmptyUsernamePassword
from services.users_service import (
    encrypt_decrypt_password,
    validate_username_password_existence,is_authenticated
)
from services.tokens_service import insert_and_get_token_for_user, set_token_in_cookie,get_token_data_by_user_id,delete_token

bp = Blueprint("api", __name__)


@bp.route("/login", methods=["POST"])
def login():
    try:
        if(is_authenticated()):
            return { "message" :"already logged in" } 

        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        validate_username_password_existence(username, password)
        user = get_user_by_username(username)
        if not user:
            raise IncorrectUsernamePassword()

        decrypted_password = encrypt_decrypt_password(user["password"])
        if decrypted_password != password:
            raise IncorrectUsernamePassword()
        user_id = user["id"]
        user_token = get_token_data_by_user_id(user_id)        
        if user_token:
            delete_token(user_token['token'])
        token_response = insert_and_get_token_for_user(user_id)
        flash(f"Hey {user["username"]}, welcome back", category="message")
        response = redirect("/books")
        return set_token_in_cookie(token_response,response)

    except (IncorrectUsernamePassword , EmptyUsernamePassword)as error:
        flash(str(error), category="error")
        return redirect(url_for("index.login", username=username))
    except (DatabaseDuplicationEntryError, Exception) as error:
        flash("An error occurred. Please try again later.", category="error")
        print(f"Error while login, error: {error}")
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
        user = get_user_by_username(username)
        flash("user created successfully", category="success")
        flash(f"Welcome {username}", category="message")
        token_response = insert_and_get_token_for_user(user["id"])
        response = redirect(url_for('index.books'))
        return set_token_in_cookie(token_response,response)
    except EmptyUsernamePassword as error:
        session.pop('_flashes', None)
        flash(str(error), category="error")
        return redirect(url_for("index.signup"))
    except DatabaseDuplicationEntryError as error:
        session.pop('_flashes', None)
        flash("Username or email already exists. Please login.", category="message")
        return redirect(url_for("index.login", username=username))
    except DatabaseOperationError as error:
        session.pop('_flashes', None)
        flash("An unexpected error occurred. Please try again later.", category="error")
        print("Error while create user" , error)
        return redirect(url_for("index.signup"))
