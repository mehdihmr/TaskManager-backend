from flask import Blueprint, jsonify, request
from app.utilities import Logger
from app.models import Task
from app import db

comment_bp = Blueprint("comment_bp", __name__)


# todo not needed anymore
@comment_bp.route("/comment/fetch", methods=["POST"])
def fetch_comments():
    """Fetches the comments of a task."""
    try:
        data: dict = request.get_json()
        id = data.get("id")

        task: Task = Task.query.get(int(id))
        if not task:
            Logger.log_error(f"{__name__} - The task with ID '{id}' does not exits.")
            return jsonify({"status": "error", "message": f"The task with ID '{id}' does not exits."}), 404

        return jsonify({"status": "success", "message": "comments fetched", "comments": task.comments}), 200
    except Exception as e:
        Logger.log_error(f"{__name__} - Error fetching the comments. {e}")
        return jsonify({"status": "error", "message": "Error fetching the comments."}), 500


@comment_bp.route("/comment/delete", methods=["POST"])
def delete_comment():
    """Deletes a comment from a task."""
    try:
        data: dict = request.get_json()
        id = data.get("id")
        comment = data.get("comment")
        if not all([id, comment]):
            Logger.log_error(f"{__name__} - Missing parameters.")
            return jsonify({"status": "error", "message": "Missing parameters."}), 400

        task: Task = Task.query.get(int(id))
        if not task:
            Logger.log_error(f"{__name__} - The task with ID '{id}' does not exits.")
            return jsonify({"status": "error", "message": f"The task with ID '{id}' does not exits."}), 404

        task.comments.remove(comment)
        db.session.commit()
        Logger.log_info(f"{__name__} - Comment '{comment}' deleted.")
        return jsonify({"status": "success", "message": "Comment deleted."}), 200

    except Exception as e:
        Logger.log_error(f"{__name__} - Error deleting the comment. {e}")
        return jsonify({"status": "error", "message": "Error deleting the comment."}), 500


@comment_bp.route("/comment/update", methods=["POST"])
def update_comment():
    """Updates a comment from a task."""
    try:
        data: dict = request.get_json()
        id = data.get("id")
        comment = data.get("comment")
        new_comment = data.get("newComment")

        if not all([id, comment, new_comment]):
            Logger.log_error(f"{__name__} - Missing parameters.")
            return jsonify({"status": "error", "message": "Missing parameters."}), 400

        task: Task = Task.query.get(int(id))
        if not task:
            Logger.log_error(f"{__name__} - The task with ID '{id}' does not exits.")
            return jsonify({"status": "error", "message": f"The task with ID '{id}' does not exits."}), 404

        idx = task.comments.index(comment)
        task.comments[idx] = new_comment
        db.session.commit()

        Logger.log_info(f"{__name__} - Comment updated.")
        return jsonify({"status": "success", "message": "Comment updated."}), 200
    except Exception as e:
        Logger.log_error(f"{__name__} - Error updating the comment. {e}")
        return jsonify({"status": "error", "message": "Error updating the comment."}), 500
