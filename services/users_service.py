from flask import redirect, url_for, flash
from config import hash_key
from functools import wraps


def requires_authentication(func):
    @wraps(func)
    def authenticated_function(*args, **kwargs):
        # need to implement is authenticated
        if False:
            flash("Must login", category="message")
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
