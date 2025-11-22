from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.task import Task
from app.models.user import User
from app.models.enums.task_status import TaskStatus
from app.models.enums.task_priority import TaskPriority
from app.utilities import Logger

task_bp = Blueprint("task_bp", __name__)


@task_bp.route("/task/fetch", methods=["GET"])
@jwt_required()
def get_tasks():
    """Gets the tasks."""
    try:
        user_id = get_jwt_identity()
        if not user_id:
            error_message = "Missing Authorization Header"
            Logger.log_error(f"{__name__} - {error_message}")
            return jsonify({"status": "error", "message": error_message}), 401

        user: User = User.query.filter_by(id=user_id).first()
        if not user:
            Logger.log_error(f"{__name__} - Error fetching the tasks")
            return jsonify({"status": "error", "message": "Error getching tht tasks"}), 400
        return (
            jsonify(
                {
                    "status": "success",
                    "tasks": [t.to_dict() for t in user.tasks],
                }
            ),
            200,
        )
    except Exception as e:
        Logger.log_error(f"{__name__} - Error querying the tasks., {e}")
        return jsonify({"status": "error", "message": "Error querying the tasks."}), 500


@task_bp.route("/task/add", methods=["POST"])
@jwt_required()
def add_task():
    """Adds a new task."""
    try:
        data: dict = request.get_json()
        title = data.get("title")
        description = data.get("description", "")
        user_id = get_jwt_identity()
        print(user_id)

        if not all([title, user_id]):
            Logger.log_error(f"{__name__} - Missing parameters.")
            return jsonify({"status": "error", "message": "Missing parameters."}), 400

        new_task = Task(title=title, description=description, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
        Logger.log_info(f"{__name__} - Task added")
        return jsonify({"message": "Task added"}), 201
    except Exception as e:
        Logger.log_info(f"{__name__} - Error adding task, {e}")
        return jsonify({"status": "error", "message": "Error adding task"}), 500


@task_bp.route("/task/update", methods=["POST"])
def update_status():
    """Updates the status of a task."""
    try:
        data: dict = request.get_json()
        id = data.get("id")
        status = data.get("status")
        title = data.get("title")
        description = data.get("description")
        priority = data.get("priority")
        comment = data.get("comment")

        if not id:
            Logger.log_error(f"{__name__} - Missing parameters.")
            return jsonify({"status": "error", "message": "Missing parameters."}), 400

        task: Task = Task.query.get(int(id))
        if not task:
            Logger.log_error(f"{__name__} - The task with ID '{id}' does not exits.")
            return jsonify({"status": "error", "message": f"The task with ID '{id}' does not exits."}), 404

        if status:
            task.status = TaskStatus(status)
        if title:
            task.title = title
        if description:
            task.description = description
        if priority:
            task.priority = TaskPriority(priority)
        if comment:
            task.comments.append(comment)

        db.session.commit()
        Logger.log_info(f"{__name__} - Task '{task.title}' updated.")
        return (
            jsonify({"status": "success", "message": f"Task '{task.title}' updated."}),
            200,
        )
    except ValueError as e:
        Logger.log_error(f"{__name__} - Error in parameter values, {e}")
        return jsonify({"status": "error", "message": f"Error in parameter values, {e}"}), 400
    except Exception as e:
        Logger.log_error(f"{__name__} - Error updating the status. {e}")
        return jsonify({"status": "error", "message": "Error updating the status."}), 500


@task_bp.route("/task/delete", methods=["POST"])
def delete_task():
    """Deletes a specifc task by id."""
    try:
        data: dict = request.get_json()
        id = data.get("id")

        if not id:
            Logger.log_error(f"{__name__} - Missing parameters.")
            return jsonify({"status": "error", "message": "Missing parameters."}), 400

        task: Task = Task.query.get(int(id))
        if not task:
            Logger.log_error(f"{__name__} - The task with ID '{id}' does not exits.")
            return jsonify({"status": "error", "message": f"The task with ID '{id}' does not exits."}), 404

        db.session.delete(task)
        db.session.commit()

        Logger.log_info(f"{__name__} - The task '{task.title}' was deleted.")
        return (
            jsonify({"status": "success", "message": f"The task '{task.title}' was deleted."}),
            200,
        )
    except ValueError as e:
        Logger.log_error(f"{__name__} - Error in parameter values, {e}")
        return jsonify({"status": "error", "message": f"Error in parameter values, {e}"}), 400
    except Exception as e:
        Logger.log_error(f"{__name__} - Error updating the status. {e}")
        return jsonify({"status": "error", "message": "Error updating the status."}), 500
