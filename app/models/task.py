from app import db
from app.models.enums.task_status import TaskStatus
from datetime import datetime


class Task(db.Model):
    """The task model.

    Args:
        db: The SQL database.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    done = db.Column(db.Enum(TaskStatus), default=TaskStatus.TODO)
    creation_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        """Gets the description of the task object.

        Returns:
            str: The description of the task object.
        """
        return f"<Task {self.title}>"
