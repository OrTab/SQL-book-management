from flask import Blueprint

bp = Blueprint("user", __name__)


@bp.route("/<user_id>")
def get_user(user_id):
    return {"answer": user_id}
