from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()
Base = declarative_base()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()