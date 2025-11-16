from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.utilities import Logger

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    """Creates a flask app with an SQL databse.

    Returns:
        Flask: A Flask app.
    """
    Logger.log_info(f"{__name__} - Starting the app...")
    app = Flask(__name__)
    CORS(app)
    app.config.from_object("config")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    Logger.log_info(f"{__name__} - Database initialized.")

    from app.routes import task_bp
    from app.routes import comment_bp
    from app.routes import auth_bp

    app.register_blueprint(task_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(auth_bp)
    Logger.log_info(f"{__name__} - API Routes initialized.")

    return app
