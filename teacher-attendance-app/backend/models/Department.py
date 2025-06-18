from database import db
from models.base import BaseModel

class Department(BaseModel):
    __tablename__ = 'departments'
    
    code = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    abbreviation = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    def get_teachers(self):
        """Get teachers for this department safely"""
        try:
            from models.teacher import Teacher
            return Teacher.query.filter_by(department_id=self.id, is_active=True).all()
        except:
            return []
    
    def get_subjects(self):
        """Get subjects for this department safely"""
        try:
            from models.subject import Subject
            return Subject.query.filter_by(department_id=self.id, is_active=True).all()
        except:
            return []
    
    def get_teachers_count(self):
        """Get teachers count for this department safely"""
        try:
            from models.teacher import Teacher
            return Teacher.query.filter_by(department_id=self.id, is_active=True).count()
        except:
            return 0
    
    def get_subjects_count(self):
        """Get subjects count for this department safely"""
        try:
            from models.subject import Subject
            return Subject.query.filter_by(department_id=self.id, is_active=True).count()
        except:
            return 0
    
    def to_dict(self):
        base_dict = super().to_dict()
        return {
            **base_dict,
            'code': self.code,
            'name': self.name,
            'abbreviation': self.abbreviation,
            'description': self.description,
            'is_active': self.is_active,
            'teacher_count': self.get_teachers_count(),
            'subject_count': self.get_subjects_count()
        }

    def __repr__(self):
        return f"<Department(code='{self.code}', name='{self.name}')>"
        

    def __repr__(self):
        return f"<Department(code='{self.code}', name='{self.name}')>"
