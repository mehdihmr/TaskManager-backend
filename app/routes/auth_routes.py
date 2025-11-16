from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.utilities import Logger
from app.models import User
from app import db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user."""
    try:
        data: dict = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not all([username, email, password]):
            Logger.log_error(f"{__name__} - Missing parameters.")
            return jsonify({"status": "error", "message": "Missing parameters."}), 400

        new_user = User(username=username, email=email, password_hash=password)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        Logger.log_info(f"{__name__} - User registered.")
        return jsonify({"status": "success", "message": "User registered."}), 201
    except Exception as e:
        Logger.log_error(f"{__name__} - Error registering user: {e}")
        return jsonify({"status": "error", "message": "Error registering user."}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate a user and return an access token."""
    data: dict = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not all([username, password]):
        Logger.log_error(f"{__name__} - Missing parameters.")
        return jsonify({"status": "error", "message": "Missing parameters."}), 400
    user: User = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        Logger.log_error(f"{__name__} - Bad credentials.")
        return jsonify({"status": "error", "message": "Bad credentials."}), 401

    access_token = create_access_token(identity=user.id)
    Logger.log_info(f"{__name__} - {user.username} logged in.")
    return jsonify({"status": "success", "access_token": access_token}), 200


@auth_bp.route("/fetch-users", methods=["GET"])
def fetch_users():
    """Fetch all users."""
    users: list[User] = User.query.all()

    return (
        jsonify(
            {
                "users": [
                    {"id": u.id, "username": u.username, "email": u.email, "password": u.password_hash} for u in users
                ]
            }
        ),
        200,
    )


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    """Get the profile of the currently authenticated user."""
    user_id = get_jwt_identity()
    return jsonify({"user_id": user_id}), 200
