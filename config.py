import os

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/inventry.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')

    # Flask-Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False