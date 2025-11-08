from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.task_routes import task_bp

    app.register_blueprint(task_bp, url_prefix="/api/tasks")

    return app
