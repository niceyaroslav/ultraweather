import os


BASE_DIR = os.path.dirname(__file__)


class Config:
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'weather.db')}"
    SECRET_KEY = b'AKDSLLDDADDADADSDASDSDAS5'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
