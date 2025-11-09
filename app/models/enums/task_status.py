from enum import Enum


class TaskStatus(Enum):
    """The enum of the task status."""

    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"
