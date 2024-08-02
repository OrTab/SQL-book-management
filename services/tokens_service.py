from flask import request, g
from services.db_service import db_operation
from config import login_token_cookie_name, host
from datetime import datetime, timedelta


def insert_and_get_token_for_user(user_id):
    query = """INSERT INTO tokens (id, token, user_id, expiration)
                    VALUES (UUID(), UUID(), %s, DATE_ADD(NOW(), INTERVAL 1 MONTH))
                """
    db_operation(query, (user_id,))
    query = """
            SELECT id, token, expiration
            FROM tokens
            WHERE user_id = %s
        """
    return db_operation(query, (user_id,), True)


def set_token_in_cookie(token, response):
    g.should_remove_auth_token_cookie = False
    response.set_cookie(
        login_token_cookie_name,
        token["token"],
        expires=token["expiration"],
        httponly=True,
    )
    return response


def remove_token_from_cookie(response):
    past_date = datetime(1970, 1, 1)
    response.set_cookie(
        login_token_cookie_name,
        "",
        expires=past_date,
        httponly=True,
    )
    return response


def get_token_data(token):
    query = "SELECT * FROM tokens WHERE token = %s"
    token_response = db_operation(query, (token,))
    return token_response[0] if token_response else None


def get_token_data_by_user_id(user_id):
    query = "SELECT * FROM tokens WHERE user_id = %s"
    token_response = db_operation(query, (user_id,))
    return token_response[0] if token_response else None


def delete_token(token):
    query = "DELETE from tokens WHERE token = %s"
    db_operation(query, (token,))


def get_token_from_cookie():
    auth_token = request.cookies.get(login_token_cookie_name)
    return auth_token or None
