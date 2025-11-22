from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """User model representing a user in the system."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.String(255), nullable=True)
    tasks = db.relationship("Task", backref="user", lazy=True)

    def set_password(self, password):
        """Set the user's password by hashing it.

        Args:
            password (str): The plaintext password to hash and store.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored password hash."""
        return check_password_hash(self.password_hash, password)
