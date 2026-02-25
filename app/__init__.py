import os
from flask import Flask

def create_app():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    app = Flask(
        __name__,
        template_folder=os.path.join(root_dir, "templates"),
        static_folder=os.path.join(root_dir, "static"),
    )

    app.secret_key = "change-me-later"

    # register routes
    from .routes import routes_bp
    app.register_blueprint(routes_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    return app