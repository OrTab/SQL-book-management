from flask import Flask, render_template, send_from_directory, g, request
from routes import index
from routes.api import auth, books, user
from config import (
    api_prefix,
    port,
    host,
    hash_key,
)
from services.tokens_service import remove_token_from_cookie
from services.users_service import is_authenticated, get_user_by_token

app = Flask(__name__)


@app.before_request
def handle_before_request():
    g.should_remove_auth_token_cookie = False
    if request.url.startswith("/static"):
        return
    if is_authenticated():
        user = get_user_by_token(g.auth_token)
        if user:
            g.user = user


@app.after_request
def handle_after_request(response):
    if g.should_remove_auth_token_cookie:
        response = remove_token_from_cookie(response)
    return response


@app.context_processor
def inject_user():
    user = g.user if hasattr(g, "user") else None
    return dict(user=user)


app.secret_key = hash_key

# main routes
app.register_blueprint(index.bp)
# auth routes
app.register_blueprint(auth.bp, url_prefix=f"{api_prefix}/auth")
# books routes
app.register_blueprint(books.bp, url_prefix=f"{api_prefix}/books")
# books routes
app.register_blueprint(user.bp, url_prefix=f"{api_prefix}/user")

if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
