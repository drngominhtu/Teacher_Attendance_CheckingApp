# Import theo thứ tự để tránh circular import
from .base import BaseModel
from .teacher import Teacher, EmployeeType, DegreeLevel
from .subject import Subject
from .semester import Semester
from .assignment import Assignment
from .schedule import Schedule
from .teaching_assignment import TeachingAssignment
from .teaching_record import TeachingRecord
from .salary_calculation import SalaryCalculation

# Import database sau khi định nghĩa models
from database import db

# Setup relationships đơn giản - sẽ setup trong app context
def setup_relationships():
    """Setup relationships between models - được gọi sau khi app khởi tạo"""
    pass  # Tạm thời để trống để tránh lỗi circular import

__all__ = [
    'BaseModel',
    'Teacher', 'EmployeeType', 'DegreeLevel',
    'Subject',
    'Semester', 
    'Assignment',
    'Schedule',
    'TeachingAssignment',
    'TeachingRecord',
    'SalaryCalculation',
    'setup_relationships'
]