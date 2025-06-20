from database import db
from datetime import datetime

class SalaryCalculation(db.Model):
    __tablename__ = 'salary_calculations'
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=True)
    calculation_date = db.Column(db.Date, default=datetime.utcnow)
    total_hours = db.Column(db.Float, default=0)
    adjusted_hours = db.Column(db.Float, default=0)
    total_amount = db.Column(db.Float, default=0)
    base_hourly_rate = db.Column(db.Float, default=100000)
    teacher_coefficient = db.Column(db.Float, default=1.0)
    notes = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)
    approved_by = db.Column(db.String(100))
    approved_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert salary calculation to dictionary"""
        try:
            # Get teacher info safely
            teacher_name = "N/A"
            department_name = "N/A"
            if self.teacher_id:
                try:
                    from models.teacher import Teacher
                    teacher = Teacher.query.get(self.teacher_id)
                    if teacher:
                        teacher_name = teacher.name
                        # Get department name safely
                        if hasattr(teacher, 'department_id') and teacher.department_id:
                            from models.Department import Department
                            department = Department.query.get(teacher.department_id)
                            if department:
                                department_name = department.name
                except Exception as e:
                    print(f"Error getting teacher info: {e}")
            
            # Get semester info safely
            semester_name = None
            semester_year = None
            if self.semester_id:
                try:
                    from models.semester import Semester
                    semester = Semester.query.get(self.semester_id)
                    if semester:
                        semester_name = semester.name
                        semester_year = str(semester.year)
                except Exception as e:
                    print(f"Error getting semester info: {e}")
            
            return {
                'id': self.id,
                'teacher_id': self.teacher_id,
                'teacher_name': teacher_name,
                'department_name': department_name,
                'semester_id': self.semester_id,
                'semester_name': semester_name,
                'semester_year': semester_year,
                'calculation_date': self.calculation_date.isoformat() if self.calculation_date else None,
                'total_hours': float(self.total_hours or 0),
                'adjusted_hours': float(self.adjusted_hours or 0),
                'total_amount': float(self.total_amount or 0),
                'base_hourly_rate': float(self.base_hourly_rate or 100000),
                'teacher_coefficient': float(self.teacher_coefficient or 1.0),
                'notes': self.notes,
                'is_approved': bool(self.is_approved),
                'approved_by': self.approved_by,
                'approved_at': self.approved_at.isoformat() if self.approved_at else None,
                'created_at': self.created_at.isoformat() if self.created_at else None
            }
        except Exception as e:
            print(f"Error in salary_calculation.to_dict(): {e}")
            return {
                'id': self.id or 0,
                'teacher_id': self.teacher_id or 0,
                'teacher_name': 'N/A',
                'department_name': 'N/A',
                'semester_id': getattr(self, 'semester_id', None),
                'semester_name': None,
                'semester_year': None,
                'calculation_date': None,
                'total_hours': 0.0,
                'adjusted_hours': 0.0,
                'total_amount': 0.0,
                'base_hourly_rate': 100000.0,
                'teacher_coefficient': 1.0,
                'notes': getattr(self, 'notes', None),
                'is_approved': False,
                'approved_by': getattr(self, 'approved_by', None),
                'approved_at': None,
                'created_at': None
            }