from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utilities import Logger
from app.models import User
from app import db
import time


user_bp = Blueprint("user", __name__)


@user_bp.route("/user/update-pass", methods=["POST"])
@jwt_required()
def update_pass():
    # todo
    """_summary_

    Returns:
        _type_: _description_
    """
    user_id = get_jwt_identity()
    data: dict = request.get_json()
    old_pass = data.get("old")
    new_pass = data.get("new")

    user: User = User.query.filter_by(id=user_id).first()
    if not user:
        Logger.log_error(f"{__name__} - Bad credentials.")
        return jsonify({"status": "error", "message": "Bad credentials."}), 401

    if not user.check_password(old_pass):
        Logger.log_error(f"{__name__} - Password incorrect.")
        return jsonify({"status": "error", "message": "Password is incorrect."}), 400

    user.set_password(new_pass)
    db.session.commit()
    return jsonify({"status": "sucess", "message": "password updated"}), 200


@user_bp.route("/user/profile", methods=["GET"])
@jwt_required()
def profile():
    """Get the profile of the currently authenticated user."""
    user_id = get_jwt_identity()
    user: User = User.query.filter_by(id=user_id).first()
    if not user:
        Logger.log_error(f"{__name__} - Bad credentials.")
        return jsonify({"status": "error", "message": "Bad credentials."}), 401

    return (
        jsonify(
            {
                "status": "success",
                "user": {"username": user.username, "email": user.email, "profile_image": user.profile_image},
            }
        ),
        200,
    )


@user_bp.route("/user/update-profile", methods=["POST"])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        user: User = User.query.filter_by(id=user_id).first()
        if not user:
            Logger.log_error(f"{__name__} - Bad credentials.")
            return jsonify({"status": "error", "message": "Bad credentials."}), 401

        username = request.form.get("username")
        email = request.form.get("email")
        file = request.files.get("profile_image")
        print(file)
        if username:
            user.username = username
        if email:
            user.email = email

        if file:
            from werkzeug.utils import secure_filename
            import os

            filename = secure_filename(file.filename)
            ext = filename.split(".")[-1].lower()
            final_name = f"user_{user.id}_{int(time.time())}.{ext}"
            print(current_app.config["UPLOAD_FOLDER"])

            save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], final_name)
            file.save(save_path)

            try:
                if user.profile_image:
                    old_path = os.path.join(current_app.config["UPLOAD_FOLDER"], user.profile_image)
                    if os.path.exists(old_path):
                        os.remove(old_path)
            except Exception:
                pass

            # Save the filename in DB
            user.profile_image = final_name

        db.session.commit()
        Logger.log_info(f"{__name__} - User updated.")
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "User updated.",
                    "user": {"username": user.username, "email": user.email, "profiel_image": user.profile_image},
                }
            ),
            200,
        )
    except Exception as e:
        Logger.log_error(f"{__name__} - Error occured, {e}")
        return jsonify({"status": "error", "message": f"Error occured, {e}"}), 500


@user_bp.route("/profile-image/<filename>", methods=["GET"])
def get_profile_image(filename):
    return send_from_directory(current_app.config["IMAGE_FOLDER"], filename)
