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
        """Convert subject to dictionary"""
        try:
            # Get department info safely
            department_name = "N/A"
            department_abbreviation = "N/A"
            if self.department_id:
                try:
                    from models.Department import Department
                    department = Department.query.get(self.department_id)
                    if department:
                        department_name = department.name
                        department_abbreviation = department.abbreviation
                except:
                    pass
            
            return {
                'id': self.id,
                'name': self.name,
                'code': self.code,
                'department_id': self.department_id,
                'department_name': department_name,
                'department_abbreviation': department_abbreviation,
                'credits': self.credits,
                'theory_hours': self.theory_hours or 0,
                'practice_hours': self.practice_hours or 0,
                'subject_coefficient': float(self.subject_coefficient) if self.subject_coefficient else 1.0,
                'difficulty_level': self.difficulty_level or 'normal',
                'description': self.description,
                'total_classes': 0,  # Can be calculated if needed
                'is_active': self.is_active,
                'created_at': self.created_at.isoformat() if self.created_at else None
            }
        except Exception as e:
            print(f"Error in subject.to_dict(): {e}")
            return {
                'id': self.id,
                'name': self.name or 'Unknown',
                'code': self.code,
                'department_id': self.department_id,
                'department_name': 'N/A',
                'department_abbreviation': 'N/A',
                'credits': self.credits or 3,
                'theory_hours': 0,
                'practice_hours': 0,
                'subject_coefficient': 1.0,
                'difficulty_level': 'normal',
                'description': self.description,
                'total_classes': 0,
                'is_active': True,
                'created_at': None
            }

    def __repr__(self):
        return f"<Subject(code='{self.code}', name='{self.name}', credits={self.credits})>"