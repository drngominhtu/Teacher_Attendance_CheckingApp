from database import db
from models.base import BaseModel

class Semester(BaseModel):
    __tablename__ = 'semesters'

    name = db.Column(db.String(100), nullable=False)  # Kì 1, Kì 2, Kì 3 (Hè)
    year = db.Column(db.Integer, nullable=False)
    academic_year = db.Column(db.String(10), nullable=True)  # 2024-2025
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    is_current = db.Column(db.Boolean, default=False)  # Kì hiện tại
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships sẽ được định nghĩa sau

    def to_dict(self):
        base_dict = super().to_dict()
        semester_dict = {
            'name': self.name,
            'year': self.year,
            'academic_year': self.academic_year,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_current': self.is_current,
            'is_active': self.is_active
        }
        return {**base_dict, **semester_dict}

    def __repr__(self):
        return f"<Semester(name='{self.name}', year={self.year})>"