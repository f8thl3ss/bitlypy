import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate, upgrade
from pydantic import ValidationError

from bitlypy.api import handle_validation_error

from .api.short_url import bp as short_url_bp
from .database import db


load_dotenv()
migrate = Migrate()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE"]
    else:
        if test_config and "DATABASE" in test_config:
            path = test_config["DATABASE"]
            app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{path}"
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Setup database
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        upgrade()
        app.register_error_handler(ValidationError, handle_validation_error)

    app.register_blueprint(short_url_bp)

    return app
