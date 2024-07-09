from flask import Flask, render_template, send_from_directory
from routes import index
from routes.api import auth, books, user
from config import api_prefix, port, host

app = Flask(__name__)

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
