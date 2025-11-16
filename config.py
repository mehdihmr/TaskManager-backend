import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'tasks.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = "e4cbd307-5096-4020-b7f0-b2d30d15f116"
