from .comment_routes import comment_bp
from .task_routes import task_bp
from .auth_routes import auth_bp

__all__ = ["comment_bp", "task_bp", "auth_bp"]
