import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///challenges.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
