from flask import Blueprint, request
from services.db_service import (
    db_operation,
    DatabaseOperationError,
)

bp = Blueprint("user", __name__)


@bp.route("/load_test")
def load_test_find_user():
    try:
        username = request.args.get("username")
        query = "SELECT * FROM users WHERE username = %s"
        response = db_operation(query, (username,))
        user = response[0] if response else None
        if user:
            return f"found {username}"
        else:
            return "not found"
    except DatabaseOperationError as error:
        return error.message, error.status_code
