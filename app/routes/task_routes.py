from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task
from app.utilities import Logger

task_bp = Blueprint("task_bp", __name__)


@task_bp.route("/", methods=["GET"])
def get_tasks():
    """Gets the tasks."""
    tasks: list[Task] = Task.query.all()
    return jsonify(
        [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "done": t.done.value,
                "creation": t.creation_date,
            }
            for t in tasks
        ]
    )


@task_bp.route("/", methods=["POST"])
def add_task():
    """Adds a new task."""
    try:
        data = request.get_json()
        new_task = Task(title=data["title"], description=data.get("description", ""))
        db.session.add(new_task)
        db.session.commit()
        Logger.log_info(f"{__name__} - Task added")
        return jsonify({"message": "Task added"}), 201
    except Exception as e:
        Logger.log_info(f"{__name__} - Error adding task, {e}")
        return jsonify({"status": "error", "message": "Error adding task"}), 500
