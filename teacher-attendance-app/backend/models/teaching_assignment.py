from database import db
from models.base import BaseModel
from datetime import datetime

class TeachingAssignment(BaseModel):
    __tablename__ = 'teaching_assignments'
    
    # Foreign keys
    teacher_id = db.Column(db.Integer, nullable=False)
    subject_id = db.Column(db.Integer, nullable=False)
    semester_id = db.Column(db.Integer, nullable=True)
    
    # Class info
    class_code = db.Column(db.String(50), nullable=False)
    class_student_count = db.Column(db.Integer, default=0)
    
    # Teaching info
    planned_hours = db.Column(db.Integer, nullable=False)
    actual_hours = db.Column(db.Integer, default=0)
    theory_hours = db.Column(db.Integer, default=0)
    practice_hours = db.Column(db.Integer, default=0)
    
    # Override coefficients
    teacher_coefficient_override = db.Column(db.Numeric(3, 2), nullable=True)
    subject_coefficient_override = db.Column(db.Numeric(3, 2), nullable=True)
    hourly_rate_override = db.Column(db.Numeric(10, 2), nullable=True)
    
    # Calculated values
    adjusted_hours = db.Column(db.Numeric(8, 2), default=0)
    total_amount = db.Column(db.Numeric(12, 2), default=0)
    
    # Time info
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    # Status
    status = db.Column(db.String(20), default='assigned')
    notes = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)
    approved_by = db.Column(db.Integer, nullable=True)
    approved_at = db.Column(db.DateTime)
    
    @property
    def effective_teacher_coefficient(self):
        if self.teacher_coefficient_override:
            return float(self.teacher_coefficient_override)
        # Get from teacher
        try:
            from models.teacher import Teacher
            teacher = Teacher.query.get(self.teacher_id)
            if teacher:
                return teacher.effective_teacher_coefficient
        except:
            pass
        return 1.3
    
    @property
    def effective_subject_coefficient(self):
        if self.subject_coefficient_override:
            return float(self.subject_coefficient_override)
        # Get from subject
        try:
            from models.subject import Subject
            subject = Subject.query.get(self.subject_id)
            if subject:
                return float(subject.subject_coefficient) if subject.subject_coefficient else 1.0
        except:
            pass
        return 1.0
    
    @property
    def effective_hourly_rate(self):
        if self.hourly_rate_override:
            return float(self.hourly_rate_override)
        # Get from teacher
        try:
            from models.teacher import Teacher
            teacher = Teacher.query.get(self.teacher_id)
            if teacher:
                return float(teacher.hourly_rate) if teacher.hourly_rate else 100000
        except:
            pass
        return 100000
    
    @property
    def class_coefficient(self):
        """Calculate class coefficient based on student count"""
        if self.class_student_count < 20:
            return -0.3
        elif self.class_student_count <= 29:
            return -0.2
        elif self.class_student_count <= 39:
            return -0.1
        elif self.class_student_count <= 49:
            return 0.0
        elif self.class_student_count <= 59:
            return 0.1
        elif self.class_student_count <= 69:
            return 0.2
        elif self.class_student_count <= 79:
            return 0.3
        else:
            return 0.4
    
    @property
    def calculated_adjusted_hours(self):
        """Calculate adjusted hours based on actual hours and coefficients"""
        return self.actual_hours * (self.effective_subject_coefficient + self.class_coefficient)
    
    @property
    def calculated_amount(self):
        """Calculate total payment amount"""
        return self.calculated_adjusted_hours * self.effective_teacher_coefficient * self.effective_hourly_rate
    
    @property
    def completion_rate(self):
        """Calculate completion rate as percentage"""
        if self.planned_hours == 0:
            return 0
        return (self.actual_hours / self.planned_hours) * 100
    
    def calculate_payment(self):
        """Update adjusted hours and total amount"""
        try:
            self.adjusted_hours = self.calculated_adjusted_hours
            self.total_amount = self.calculated_amount
            print(f"Payment calculated: {self.adjusted_hours} hours, {self.total_amount} VND")
        except Exception as e:
            print(f"Error calculating payment: {e}")
            self.adjusted_hours = 0
            self.total_amount = 0
    
    def get_teacher(self):
        """Get teacher safely"""
        try:
            from models.teacher import Teacher
            return Teacher.query.get(self.teacher_id)
        except:
            return None
    
    def get_subject(self):
        """Get subject safely"""
        try:
            from models.subject import Subject
            return Subject.query.get(self.subject_id)
        except:
            return None
    
    def get_semester(self):
        """Get semester safely"""
        try:
            from models.semester import Semester
            return Semester.query.get(self.semester_id)
        except:
            return None
    
    def to_dict(self):
        base_dict = super().to_dict()
        
        # Get related objects
        teacher = self.get_teacher()
        subject = self.get_subject()
        semester = self.get_semester()
        
        return {
            **base_dict,
            'teacher_id': self.teacher_id,
            'subject_id': self.subject_id,
            'semester_id': self.semester_id,
            'class_code': self.class_code,
            'class_student_count': self.class_student_count,
            'planned_hours': self.planned_hours,
            'actual_hours': self.actual_hours,
            'theory_hours': self.theory_hours,
            'practice_hours': self.practice_hours,
            
            # Related objects
            'teacher_name': teacher.name if teacher else 'N/A',
            'teacher_department': teacher.get_department_info().name if teacher and teacher.get_department_info() else 'N/A',
            'subject_name': subject.name if subject else 'N/A',
            'subject_department': subject.get_department_info().name if subject and subject.get_department_info() else 'N/A',
            'semester_name': semester.name if semester else 'N/A',
            'semester_year': semester.year if semester else None,
            
            # Effective values
            'effective_teacher_coefficient': self.effective_teacher_coefficient,
            'effective_subject_coefficient': self.effective_subject_coefficient,
            'effective_hourly_rate': self.effective_hourly_rate,
            
            # Calculated values
            'class_coefficient': self.class_coefficient,
            'calculated_adjusted_hours': self.calculated_adjusted_hours,
            'calculated_amount': self.calculated_amount,
            'completion_rate': self.completion_rate,
            
            # Other fields
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'notes': self.notes,
            'is_approved': self.is_approved,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None
        }

    def __repr__(self):
        return f"<TeachingAssignment(class_code='{self.class_code}', teacher_id={self.teacher_id})>"