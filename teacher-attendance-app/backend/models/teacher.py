from database import db
from models.base import BaseModel
import enum
from datetime import datetime

class EmployeeType(enum.Enum):
    LECTURER = "lecturer"
    ADMIN_STAFF = "admin_staff"
    RESEARCHER = "researcher"
    MANAGER = "manager"

class Teacher(BaseModel):
    __tablename__ = 'teachers'

    # Basic info columns
    employee_code = db.Column(db.String(20), unique=True, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    
    # Compatibility with old structure
    department = db.Column(db.String(100), nullable=True)
    degree_level = db.Column(db.String(20), default='dai_hoc')
    
    # Foreign key columns with proper references
    birth_date = db.Column(db.Date, nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True, default=1)
    degree_id = db.Column(db.Integer, db.ForeignKey('degrees.id'), nullable=True, default=1)
    
    # Other columns
    position = db.Column(db.String(100), nullable=True)
    qualifications = db.Column(db.String(200), nullable=True)
    academic_rank = db.Column(db.String(50), nullable=True)
    employee_type = db.Column(db.String(20), default='lecturer')
    base_salary = db.Column(db.Numeric(12, 2), default=0)
    hourly_rate = db.Column(db.Numeric(10, 2), default=100000)
    teacher_coefficient = db.Column(db.Numeric(3, 2), default=1.3)
    teacher_coefficient_override = db.Column(db.Numeric(3, 2), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    hire_date = db.Column(db.DateTime, nullable=True)
    
    # Remove complex relationships for now to avoid circular imports
    @property
    def effective_teacher_coefficient(self):
        if self.teacher_coefficient_override:
            return float(self.teacher_coefficient_override)
        elif self.teacher_coefficient:
            return float(self.teacher_coefficient)
        else:
            return 1.3
    
    @property
    def age(self):
        if self.birth_date:
            today = datetime.now().date()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
    def get_department_info(self):
        """Get department info safely without relationship"""
        if self.department_id:
            try:
                from models.Department import Department
                return Department.query.get(self.department_id)
            except:
                return None
        return None
    
    def get_degree_info(self):
        """Get degree info safely without relationship"""
        if self.degree_id:
            try:
                from models.degree import Degree
                return Degree.query.get(self.degree_id)
            except:
                return None
        return None

    def to_dict(self):
        base_dict = super().to_dict()
        
        # Get related data safely
        try:
            dept_info = self.get_department_info()
            degree_info = self.get_degree_info()
        except:
            dept_info = None
            degree_info = None
        
        return {
            **base_dict,
            'employee_code': self.employee_code,
            'name': self.name,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'phone': self.phone,
            'email': self.email,
            'department': self.department,
            'department_id': self.department_id,
            'degree_id': self.degree_id,
            'degree_level': self.degree_level,
            'position': self.position,
            'qualifications': self.qualifications,
            'academic_rank': self.academic_rank,
            'employee_type': self.employee_type,
            'base_salary': float(self.base_salary) if self.base_salary else 0,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else 0,
            'teacher_coefficient': float(self.teacher_coefficient) if self.teacher_coefficient else 1.3,
            'effective_teacher_coefficient': self.effective_teacher_coefficient,
            'is_active': self.is_active,
            'age': self.age,
            # Related data
            'department_name': dept_info.name if dept_info else (self.department or 'N/A'),
            'department_abbreviation': dept_info.abbreviation if dept_info else 'N/A',
            'degree_name': degree_info.name if degree_info else 'N/A',
            'degree_abbreviation': degree_info.abbreviation if degree_info else 'N/A'
        }

    def __repr__(self):
        return f"<Teacher(name='{self.name}')>"