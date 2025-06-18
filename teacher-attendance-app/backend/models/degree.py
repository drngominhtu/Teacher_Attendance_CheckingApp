from database import db
from models.base import BaseModel

class Degree(BaseModel):
    __tablename__ = 'degrees'
    
    name = db.Column(db.String(100), nullable=False, unique=True)
    abbreviation = db.Column(db.String(20), nullable=False)
    coefficient = db.Column(db.Numeric(3, 2), nullable=False, default=1.0)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    def get_teachers(self):
        """Get teachers with this degree safely"""
        try:
            from models.teacher import Teacher
            return Teacher.query.filter_by(degree_id=self.id, is_active=True).all()
        except:
            return []
    
    def to_dict(self):
        base_dict = super().to_dict()
        degree_dict = {
            'name': self.name,
            'abbreviation': self.abbreviation,
            'coefficient': float(self.coefficient) if self.coefficient else 1.0,
            'description': self.description,
            'is_active': self.is_active,
            'teacher_count': len(self.get_teachers())
        }
        return {**base_dict, **degree_dict}

    def __repr__(self):
        return f"<Degree(name='{self.name}', coefficient={self.coefficient})>"
    def __repr__(self):
        return f"<Degree(name='{self.name}', coefficient={self.coefficient})>"
