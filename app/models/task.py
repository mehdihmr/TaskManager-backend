from app import db
from app.models.enums.task_status import TaskStatus
from app.models.enums.task_priority import TaskPriority
from datetime import datetime
from sqlalchemy.ext.mutable import MutableList


class Task(db.Model):
    """The task model."""

    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.TODO)
    priority = db.Column(db.Enum(TaskPriority), default=TaskPriority.LOW)
    comments = db.Column(MutableList.as_mutable(db.JSON), nullable=False, default=list)
    creation_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        """Gets the description of the task object.

        Returns:
            str: The description of the task object.
        """
        return f"<Task {self.title}>"

    def to_dict(self) -> dict:
        """Gets the dictionary presentation of the task object.

        Returns:
            dict: The created dictionary (object).
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "comments": self.comments,
            "creation": self.creation_date.isoformat() + "Z",
            "user_id": self.user_id,
        }
