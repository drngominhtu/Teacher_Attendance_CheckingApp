from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialize database with app"""
    db.init_app(app)
    with app.app_context():
        # Import all models to ensure they're registered
        import models
        
        db.create_all()
        print("Database tables created successfully!")

def get_db():
    """Get database session"""
    return db.session