from flask import redirect, url_for, flash, request, Response, g
from config import (
    hash_key,
    login_token_cookie_name,
)
from functools import wraps
from error_entities.empty_username_password_error import EmptyUsernamePassword
from error_entities.auth_token_error import AuthTokenError
from services.db_service import db_operation
from services.tokens_service import (
    get_token_from_cookie,
    delete_token,
    get_token_from_db,
)
from datetime import datetime


def get_user_by_username(username):
    query = "SELECT * FROM users WHERE username = %s"
    user_response = db_operation(query, (username,))
    return user_response[0] if user_response else None


def is_authenticated():
    return handle_authenticated(False)


def handle_authenticated(is_guard_check):
    try:
        token = get_token_from_cookie()
        if token is None:
            raise AuthTokenError("Must login first")

        token_data = get_token_from_db(token)
        if not token_data:
            raise AuthTokenError("Auth token is not valid")

        is_token_expired = token_data["expiration"] <= datetime.now()
        if is_token_expired:
            delete_token(token)
            raise AuthTokenError("Token expired, please login again")
        return True
    except AuthTokenError as error:
        g.should_remove_auth_token_cookie = True
        if is_guard_check:
            flash(str(error), category="message")
            return redirect(url_for("index.login"))

        return False


def requires_authentication(func):
    @wraps(func)
    def authenticated_function(*args, **kwargs):
        result = handle_authenticated(True)
        if isinstance(result, Response):
            return result
        return func(*args, **kwargs)

    return authenticated_function


def validate_username_password_existence(username, password):
    if not username or not password:
        raise EmptyUsernamePassword()


def encrypt_decrypt_password(password):
    _password = ""
    for i, char in enumerate(password):
        hashed_char = chr(ord(char) ^ ord(hash_key[i % len(hash_key)]))
        _password += hashed_char
    return _password
