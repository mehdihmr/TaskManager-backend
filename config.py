import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'tasks.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
UPLOAD_FOLDER = "app/assets/profile_images"
IMAGE_FOLDER = "assets/profile_images"
# MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB limit
