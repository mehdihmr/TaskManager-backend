from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__)


@task_bp.route("/", methods=["GET"])
def get_tasks():
    tasks: list[Task] = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "description": t.description, "done": t.done} for t in tasks])


@task_bp.route("/", methods=["POST"])
def add_task():
    data = request.get_json()
    new_task = Task(title=data["title"], description=data.get("description", ""))
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added"}), 201
