from enum import Enum


class TaskStatus(Enum):
    """The enum of the task status."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
