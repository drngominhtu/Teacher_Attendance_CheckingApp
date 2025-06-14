from database import db
from datetime import datetime

class BaseModel(db.Model):
    """Base model with common fields and methods"""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Save instance to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error saving {self.__class__.__name__}: {e}")
            return False
    
    def delete(self):
        """Delete instance from database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting {self.__class__.__name__}: {e}")
            return False
    
    def to_dict(self):
        """Convert instance to dictionary"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_by_id(cls, id):
        """Get instance by ID"""
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def get_all(cls):
        """Get all instances"""
        return cls.query.all()