from database import db
from models.base import BaseModel
from sqlalchemy import Enum
import enum

class EmployeeType(enum.Enum):
    LECTURER = "lecturer"        # Giảng viên
    ADMIN_STAFF = "admin_staff"  # Nhân viên hành chính
    RESEARCHER = "researcher"    # Nghiên cứu viên
    MANAGER = "manager"         # Quản lý

class DegreeLevel(enum.Enum):
    DAI_HOC = "dai_hoc"         # Đại học - 1.3
    THAC_SI = "thac_si"         # Thạc sĩ - 1.5
    TIEN_SI = "tien_si"         # Tiến sĩ - 1.7
    PHO_GIAO_SU = "pho_giao_su" # Phó giáo sư - 2.0
    GIAO_SU = "giao_su"         # Giáo sư - 2.5

class Teacher(BaseModel):
    __tablename__ = 'teachers'

    name = db.Column(db.String(100), nullable=False)
    employee_code = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    department = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=True)  # Chức vụ
    qualifications = db.Column(db.String(200), nullable=True)  # Trình độ học vấn
    academic_rank = db.Column(db.String(50), nullable=True)  # Học hàm (GS, PGS, TS...)
    degree = db.Column(db.String(50), nullable=True)  # Học vị (Thạc sĩ, Tiến sĩ...)
    degree_level = db.Column(db.String(20), default='dai_hoc')  # Lưu dưới dạng string
    employee_type = db.Column(db.String(20), default='lecturer')  # Lưu dưới dạng string
    base_salary = db.Column(db.Numeric(12, 2), default=0)  # Lương cơ bản
    hourly_rate = db.Column(db.Numeric(10, 2), default=100000)  # Tiền dạy một tiết
    teacher_coefficient = db.Column(db.Numeric(3, 2), default=1.3)  # Hệ số giáo viên
    is_active = db.Column(db.Boolean, default=True)
    hire_date = db.Column(db.DateTime, nullable=True)
    
    @property
    def degree_level_enum(self):
        """Chuyển string thành enum để xử lý"""
        try:
            return DegreeLevel(self.degree_level)
        except (ValueError, TypeError):
            return DegreeLevel.DAI_HOC
    
    @property
    def employee_type_enum(self):
        """Chuyển string thành enum để xử lý"""
        try:
            return EmployeeType(self.employee_type)
        except (ValueError, TypeError):
            return EmployeeType.LECTURER
    
    @property
    def auto_teacher_coefficient(self):
        """Tự động tính hệ số giáo viên dựa trên bằng cấp"""
        coefficient_map = {
            'dai_hoc': 1.3,
            'thac_si': 1.5,
            'tien_si': 1.7,
            'pho_giao_su': 2.0,
            'giao_su': 2.5
        }
        return coefficient_map.get(self.degree_level, 1.3)
    
    def update_teacher_coefficient(self):
        """Cập nhật hệ số giáo viên dựa trên bằng cấp"""
        self.teacher_coefficient = self.auto_teacher_coefficient

    @property
    def degree_level_display(self):
        """Hiển thị tên bằng cấp tiếng Việt"""
        display_map = {
            'dai_hoc': 'Đại học',
            'thac_si': 'Thạc sĩ',
            'tien_si': 'Tiến sĩ',
            'pho_giao_su': 'Phó giáo sư',
            'giao_su': 'Giáo sư'
        }
        return display_map.get(self.degree_level, 'Đại học')

    def to_dict(self):
        base_dict = super().to_dict()
        teacher_dict = {
            'name': self.name,
            'employee_code': self.employee_code,
            'email': self.email,
            'phone': self.phone,
            'department': self.department,
            'position': self.position,
            'qualifications': self.qualifications,
            'academic_rank': self.academic_rank,
            'degree': self.degree,
            'degree_level': self.degree_level,
            'degree_level_display': self.degree_level_display,
            'employee_type': self.employee_type,
            'base_salary': float(self.base_salary) if self.base_salary else 0,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else 0,
            'teacher_coefficient': float(self.teacher_coefficient) if self.teacher_coefficient else 1.3,
            'auto_teacher_coefficient': self.auto_teacher_coefficient,
            'is_active': self.is_active,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None
        }
        return {**base_dict, **teacher_dict}

    def __repr__(self):
        return f"<Teacher(name='{self.name}', department='{self.department}', coefficient={self.teacher_coefficient})>"