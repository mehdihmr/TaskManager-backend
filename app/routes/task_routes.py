from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task
from app.models.enums.task_status import TaskStatus
from app.utilities import Logger

task_bp = Blueprint("task_bp", __name__)


@task_bp.route("/fetch", methods=["GET"])
def get_tasks():
    """Gets the tasks."""
    try:
        tasks: list[Task] = Task.query.all()
        return (
            jsonify(
                {
                    "status": "success",
                    "tasks": [
                        {
                            "id": t.id,
                            "title": t.title,
                            "description": t.description,
                            "done": t.status.value,
                            "creation": t.creation_date,
                        }
                        for t in tasks
                    ],
                }
            ),
            200,
        )
    except Exception as e:
        Logger.log_error(f"{__name__} - Error querying the tasks., {e}")
        return jsonify({"status": "error", "message": "Error querying the tasks."}), 500


@task_bp.route("/add", methods=["POST"])
def add_task():
    """Adds a new task."""
    try:
        data: dict = request.get_json()
        title = data.get("title")
        description = data.get("description", "")

        if not title:
            Logger.log_error(f"{__name__} - Missing parameters.")
            return jsonify({"status": "error", "message": "Missing parameters."}), 400

        new_task = Task(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()
        Logger.log_info(f"{__name__} - Task added")
        return jsonify({"message": "Task added"}), 201
    except Exception as e:
        Logger.log_info(f"{__name__} - Error adding task, {e}")
        return jsonify({"status": "error", "message": "Error adding task"}), 500


@task_bp.route("/update-status", methods=["POST"])
def update_status():
    """Updates the status of a task."""
    try:
        data: dict = request.get_json()
        id = data.get("id")
        status = data.get("status")

        if not all([id, status]):
            Logger.log_error(f"{__name__} - Missing parameters.")
            return jsonify({"status": "error", "message": "Missing parameters."}), 400

        task: Task = Task.query.get(int(id))
        if not task:
            Logger.log_error(f"{__name__} - The task with ID '{id}' does not exits.")
            return jsonify({"status": "error", "message": f"The task with ID '{id}' does not exits."}), 404

        task.status = TaskStatus(status)

        db.session.commit()
        Logger.log_info(f"{__name__} - Status of '{task.title}' was updated to '{task.status}'.")
        return (
            jsonify(
                {"status": "success", "message": f"Status of '{task.title}' was updated to '{task.status.value}'."}
            ),
            200,
        )
    except ValueError as e:
        Logger.log_error(f"{__name__} - Error in parameter values, {e}")
        return jsonify({"status": "error", "message": f"Error in parameter values, {e}"}), 400
    except Exception as e:
        Logger.log_error(f"{__name__} - Error updating the status. {e}")
        return jsonify({"status": "error", "message": "Error updating the status."}), 500


@task_bp.route("/delete", methods=["POST"])
def delete_task():
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
