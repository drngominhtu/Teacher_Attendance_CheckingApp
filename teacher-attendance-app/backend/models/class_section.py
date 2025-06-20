from database import db
from datetime import datetime

class ClassSection(db.Model):
    __tablename__ = 'class_sections'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    student_count = db.Column(db.Integer, default=0)
    max_students = db.Column(db.Integer, default=50)
    classroom = db.Column(db.String(50))
    schedule_info = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='planned')  # planned, active, completed, cancelled
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert class section to dictionary"""
        try:
            # Get subject info safely
            subject_name = "N/A"
            subject_credits = 0
            if self.subject_id:
                try:
                    from models.subject import Subject
                    subject = Subject.query.get(self.subject_id)
                    if subject:
                        subject_name = subject.name
                        subject_credits = subject.credits or 0
                except Exception as e:
                    print(f"Error getting subject: {e}")
            
            # Get semester info safely
            semester_name = "N/A"
            semester_year = "N/A"
            if self.semester_id:
                try:
                    from models.semester import Semester
                    semester = Semester.query.get(self.semester_id)
                    if semester:
                        semester_name = semester.name
                        semester_year = str(semester.year)
                except Exception as e:
                    print(f"Error getting semester: {e}")
            
            # Get teacher info safely
            teacher_name = None
            teacher_department = None
            if self.teacher_id:
                try:
                    from models.teacher import Teacher
                    teacher = Teacher.query.get(self.teacher_id)
                    if teacher:
                        teacher_name = teacher.name
                        if hasattr(teacher, 'department_abbreviation'):
                            teacher_department = teacher.department_abbreviation
                except Exception as e:
                    print(f"Error getting teacher: {e}")
            
            return {
                'id': self.id,
                'code': self.code,
                'name': self.name,
                'subject_id': self.subject_id,
                'subject_name': subject_name,
                'subject_credits': subject_credits,
                'semester_id': self.semester_id,
                'semester_name': semester_name,
                'semester_year': semester_year,
                'teacher_id': self.teacher_id,
                'teacher_name': teacher_name,
                'teacher_department': teacher_department,
                'student_count': self.student_count or 0,
                'max_students': self.max_students or 50,
                'classroom': self.classroom,
                'schedule_info': self.schedule_info,
                'start_date': self.start_date.isoformat() if self.start_date else None,
                'end_date': self.end_date.isoformat() if self.end_date else None,
                'notes': self.notes,
                'status': self.status or 'planned',
                'is_active': self.is_active,
                'created_at': self.created_at.isoformat() if self.created_at else None
            }
        except Exception as e:
            print(f"Error in class_section.to_dict(): {e}")
            # Return basic data if error occurs
            return {
                'id': self.id,
                'code': self.code or 'N/A',
                'name': self.name or 'N/A',
                'subject_id': self.subject_id,
                'subject_name': 'N/A',
                'subject_credits': 0,
                'semester_id': self.semester_id,
                'semester_name': 'N/A',
                'semester_year': 'N/A',
                'teacher_id': self.teacher_id,
                'teacher_name': None,
                'teacher_department': None,
                'student_count': self.student_count or 0,
                'max_students': self.max_students or 50,
                'classroom': self.classroom,
                'schedule_info': self.schedule_info,
                'start_date': None,
                'end_date': None,
                'notes': self.notes,
                'status': self.status or 'planned',
                'is_active': True,
                'created_at': None
            }
    
    def save(self):
        """Save class section to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error saving class section: {e}")
            return False
    
    def delete(self):
        """Delete class section from database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting class section: {e}")
            return False
    
    @staticmethod
    def get_by_id(id):
        """Get class section by ID"""
        try:
            return ClassSection.query.get(id)
        except Exception as e:
            print(f"Error getting class section by ID: {e}")
        return None
    
    def __repr__(self):
        return f"<ClassSection(code='{self.code}', name='{self.name}', status='{self.status}')>"
