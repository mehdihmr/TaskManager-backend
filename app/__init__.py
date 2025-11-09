from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from app.utilities import Logger

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Creates a flask app with an SQL databse.

    Returns:
        Flask: A Flask app.
    """
    Logger.log_info(f"{__name__} - Starting the app...")
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)
    migrate.init_app(app, db)
    Logger.log_info(f"{__name__} - Database initialized.")

    from app.routes.task_routes import task_bp

    app.register_blueprint(task_bp)
    Logger.log_info(f"{__name__} - API Routes initialized.")

    return app
