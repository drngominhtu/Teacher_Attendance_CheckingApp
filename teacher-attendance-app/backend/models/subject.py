from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text, ForeignKey
from database import db
from models.base import BaseModel

class Subject(BaseModel):
    __tablename__ = 'subjects'

    # Basic info
    code = db.Column(db.String(20), unique=True, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, default=3)
    
    # Foreign key with proper reference
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True, default=1)
    
    # Detail info
    theory_hours = db.Column(db.Integer, default=0)
    practice_hours = db.Column(db.Integer, default=0)
    total_hours = db.Column(db.Integer, default=0)
    subject_coefficient = db.Column(db.Numeric(3, 2), default=1.0)
    difficulty_level = db.Column(db.String(20), default='normal')
    description = db.Column(db.Text, nullable=True)
    prerequisites = db.Column(db.Text, nullable=True)
    
    # Compatibility
    department = db.Column(db.String(100), nullable=True)
    student_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    
    # Define relationship
    department_ref = db.relationship('Department', foreign_keys=[department_id], backref='subjects')
    
    @property
    def total_classes(self):
        """Count teaching assignments for this subject"""
        try:
            from models.teaching_assignment import TeachingAssignment
            return TeachingAssignment.query.filter_by(subject_id=self.id).count()
        except:
            return 0
    
    def get_department_info(self):
        """Get department info using relationship"""
        return self.department_ref

    def to_dict(self):
        base_dict = super().to_dict()
        dept_info = self.get_department_info()
        
        return {
            **base_dict,
            'code': self.code,
            'name': self.name,
            'credits': self.credits,
            'department_id': self.department_id,
            'theory_hours': self.theory_hours,
            'practice_hours': self.practice_hours,
            'total_hours': self.total_hours,
            'subject_coefficient': float(self.subject_coefficient) if self.subject_coefficient else 1.0,
            'difficulty_level': self.difficulty_level,
            'description': self.description,
            'prerequisites': self.prerequisites,
            'department': self.department,
            'student_count': self.student_count,
            'is_active': self.is_active,
            'total_classes': self.total_classes,
            'total_students': self.student_count,
            # Related data via relationship
            'department_name': dept_info.name if dept_info else (self.department or 'N/A'),
            'department_code': dept_info.code if dept_info else 'N/A',
            'department_abbreviation': dept_info.abbreviation if dept_info else 'N/A'
        }

    def __repr__(self):
        return f"<Subject(code='{self.code}', name='{self.name}', credits={self.credits})>"