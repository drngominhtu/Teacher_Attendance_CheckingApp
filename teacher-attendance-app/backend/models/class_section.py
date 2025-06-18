from database import db
from models.base import BaseModel
from datetime import datetime

class ClassSection(BaseModel):
    __tablename__ = 'class_sections'
    
    # Basic information
    code = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    
    # Foreign keys
    subject_id = db.Column(db.Integer, nullable=False)
    semester_id = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, nullable=True)
    
    # Class details
    student_count = db.Column(db.Integer, default=0)
    max_students = db.Column(db.Integer, default=50)
    classroom = db.Column(db.String(50))
    schedule_info = db.Column(db.String(200))
    
    # Dates
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # Status and notes
    status = db.Column(db.String(20), default='planned')  # planned, active, completed, cancelled
    notes = db.Column(db.Text)
    
    @property
    def enrollment_rate(self):
        """Calculate enrollment rate as percentage"""
        if self.max_students == 0:
            return 0
        return (self.student_count / self.max_students) * 100
    
    @property
    def class_coefficient(self):
        """Calculate class coefficient based on student count"""
        if self.student_count < 20:
            return -0.3
        elif self.student_count <= 29:
            return -0.2
        elif self.student_count <= 39:
            return -0.1
        elif self.student_count <= 49:
            return 0.0
        elif self.student_count <= 59:
            return 0.1
        elif self.student_count <= 69:
            return 0.2
        elif self.student_count <= 79:
            return 0.3
        else:
            return 0.4
    
    @property
    def is_full(self):
        """Check if class is full"""
        return self.student_count >= self.max_students
    
    @property
    def available_slots(self):
        """Get number of available slots"""
        return max(0, self.max_students - self.student_count)
    
    def get_subject_info(self):
        """Get subject information safely"""
        try:
            from models.subject import Subject
            return Subject.query.get(self.subject_id)
        except:
            return None
    
    def get_semester_info(self):
        """Get semester information safely"""
        try:
            from models.semester import Semester
            return Semester.query.get(self.semester_id)
        except:
            return None
    
    def get_teacher_info(self):
        """Get teacher information safely"""
        if not self.teacher_id:
            return None
        try:
            from models.teacher import Teacher
            return Teacher.query.get(self.teacher_id)
        except:
            return None
    
    def assign_teacher(self, teacher_id):
        """Assign a teacher to this class section"""
        self.teacher_id = teacher_id
        return self.save()
    
    def update_enrollment(self, new_count):
        """Update student enrollment count"""
        if 0 <= new_count <= self.max_students:
            self.student_count = new_count
            return self.save()
        return False
    
    def activate(self):
        """Activate the class section"""
        self.status = 'active'
        return self.save()
    
    def complete(self):
        """Mark class section as completed"""
        self.status = 'completed'
        return self.save()
    
    def cancel(self):
        """Cancel the class section"""
        self.status = 'cancelled'
        return self.save()
    
    def to_dict(self):
        """Convert to dictionary with related data"""
        base_dict = super().to_dict()
        
        # Get related objects
        subject_info = self.get_subject_info()
        semester_info = self.get_semester_info()
        teacher_info = self.get_teacher_info()
        
        # Build result dictionary
        result = {
            **base_dict,
            'code': self.code,
            'name': self.name,
            'subject_id': self.subject_id,
            'semester_id': self.semester_id,
            'teacher_id': self.teacher_id,
            'student_count': self.student_count,
            'max_students': self.max_students,
            'classroom': self.classroom,
            'schedule_info': self.schedule_info,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'notes': self.notes,
            'is_active': self.is_active,
            
            # Calculated properties
            'enrollment_rate': round(self.enrollment_rate, 2),
            'class_coefficient': self.class_coefficient,
            'is_full': self.is_full,
            'available_slots': self.available_slots,
            
            # Related data
            'subject_name': subject_info.name if subject_info else None,
            'subject_code': subject_info.code if subject_info else None,
            'subject_credits': subject_info.credits if subject_info else None,
            'semester_name': semester_info.name if semester_info else None,
            'semester_year': semester_info.year if semester_info else None,
            'teacher_name': teacher_info.name if teacher_info else None,
            'teacher_department': None
        }
        
        # Add teacher department info safely
        if teacher_info:
            try:
                dept_info = teacher_info.get_department_info()
                if dept_info:
                    result['teacher_department'] = dept_info.name
            except:
                pass
        
        return result
    
    def __repr__(self):
        return f"<ClassSection(code='{self.code}', name='{self.name}', status='{self.status}')>"
