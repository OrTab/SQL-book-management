from flask import redirect, url_for, flash, request
from config import hash_key, login_token_cookie_name
from functools import wraps


def is_authenticated():
    auth_token = request.cookies.get(login_token_cookie_name)
    return auth_token is not None


def requires_authentication(func):
    @wraps(func)
    def authenticated_function(*args, **kwargs):
        # need to implement is authenticated
        if not is_authenticated():
            flash("Must login first", category="message")
            return redirect(url_for("index.login"))
        return func(*args, **kwargs)

    return authenticated_function


def validate_username_password_existence(username, password):
    if not username or not password:
        raise ValueError("Username or password cannot be empty.")


def encrypt_decrypt_password(password):
    _password = ""
    for i, char in enumerate(password):
        hashed_char = chr(ord(char) ^ ord(hash_key[i % len(hash_key)]))
        _password += hashed_char
    return _password
