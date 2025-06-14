import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///teacher_attendance.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')