from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text
from database import db
from models.base import BaseModel

class Subject(BaseModel):
    __tablename__ = 'subjects'

    name = db.Column(db.String(200), nullable=False)
    subject_code = db.Column(db.String(20), unique=True, nullable=True)
    department = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False, default=3)  # Số tín chỉ
    theory_hours = db.Column(db.Integer, default=0)  # Số giờ lý thuyết
    practice_hours = db.Column(db.Integer, default=0)  # Số giờ thực hành
    student_count = db.Column(db.Integer, default=0)  # Số sinh viên
    standard_rate = db.Column(db.Numeric(10, 2), default=0)  # Đơn giá chuẩn
    subject_coefficient = db.Column(db.Numeric(3, 2), default=1.0)  # Hệ số học phần (1.0 - 1.5)
    difficulty_level = db.Column(db.String(20), default='normal')  # easy, normal, hard, very_hard
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    @property
    def total_hours(self):
        return self.theory_hours + self.practice_hours
    
    @property
    def class_coefficient(self):
        """Tính hệ số lớp dựa trên số sinh viên"""
        if self.student_count < 20:
            return -0.3
        elif 20 <= self.student_count <= 29:
            return -0.2
        elif 30 <= self.student_count <= 39:
            return -0.1
        elif 40 <= self.student_count <= 49:
            return 0.0
        elif 50 <= self.student_count <= 59:
            return 0.1
        elif 60 <= self.student_count <= 69:
            return 0.2
        elif 70 <= self.student_count <= 79:
            return 0.3
        else:  # >= 80
            return 0.4

    def to_dict(self):
        base_dict = super().to_dict()
        subject_dict = {
            'name': self.name,
            'subject_code': self.subject_code,
            'department': self.department,
            'credits': self.credits,
            'theory_hours': self.theory_hours,
            'practice_hours': self.practice_hours,
            'total_hours': self.total_hours,
            'student_count': self.student_count,
            'standard_rate': float(self.standard_rate) if self.standard_rate else 0,
            'subject_coefficient': float(self.subject_coefficient) if self.subject_coefficient else 1.0,
            'class_coefficient': self.class_coefficient,
            'difficulty_level': self.difficulty_level,
            'description': self.description,
            'is_active': self.is_active
        }
        return {**base_dict, **subject_dict}

    def __repr__(self):
        return f"<Subject(name='{self.name}', students={self.student_count}, subject_coeff={self.subject_coefficient})>"