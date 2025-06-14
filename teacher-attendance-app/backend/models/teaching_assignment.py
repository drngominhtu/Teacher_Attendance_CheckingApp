from database import db
from models.base import BaseModel
from datetime import datetime

class TeachingAssignment(BaseModel):
    __tablename__ = 'teaching_assignments'
    
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=True)
    class_code = db.Column(db.String(50), nullable=False)  # Mã lớp
    
    # Thông tin lớp học
    class_student_count = db.Column(db.Integer, default=0)  # Số sinh viên thực tế của lớp này
    
    # Thông tin giảng dạy
    planned_hours = db.Column(db.Integer, nullable=False)  # Số tiết dự kiến
    actual_hours = db.Column(db.Integer, default=0)        # Số tiết thực tế đã dạy
    theory_hours = db.Column(db.Integer, default=0)        # Tiết lý thuyết
    practice_hours = db.Column(db.Integer, default=0)      # Tiết thực hành
    
    # Hệ số tính tiền (có thể override từ teacher và subject)
    teacher_coefficient_override = db.Column(db.Numeric(3, 2), nullable=True)  # Override hệ số giáo viên
    subject_coefficient_override = db.Column(db.Numeric(3, 2), nullable=True)  # Override hệ số học phần
    hourly_rate_override = db.Column(db.Numeric(10, 2), nullable=True)         # Override tiền dạy một tiết
    
    # Thông tin tài chính (tính toán tự động)
    adjusted_hours = db.Column(db.Numeric(8, 2), default=0)    # Số tiết quy đổi
    total_amount = db.Column(db.Numeric(12, 2), default=0)     # Tổng tiền dạy
    
    # Thời gian
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    # Trạng thái
    status = db.Column(db.String(20), default='assigned')  # assigned, in_progress, completed, cancelled
    notes = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)     # Đã duyệt chưa
    approved_by = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    approved_at = db.Column(db.DateTime)
    
    # Relationships
    teacher = db.relationship('Teacher', foreign_keys=[teacher_id], backref='teaching_assignments')
    subject = db.relationship('Subject', foreign_keys=[subject_id], backref='teaching_assignments')
    semester = db.relationship('Semester', foreign_keys=[semester_id], backref='teaching_assignments')
    approver = db.relationship('Teacher', foreign_keys=[approved_by])
    
    @property
    def effective_teacher_coefficient(self):
        """Hệ số giáo viên hiệu lực (ưu tiên override, nếu không thì lấy từ teacher)"""
        if self.teacher_coefficient_override:
            return float(self.teacher_coefficient_override)
        elif self.teacher:
            return float(self.teacher.teacher_coefficient)
        else:
            return 1.3  # Mặc định
    
    @property
    def effective_subject_coefficient(self):
        """Hệ số học phần hiệu lực (ưu tiên override, nếu không thì lấy từ subject)"""
        if self.subject_coefficient_override:
            return float(self.subject_coefficient_override)
        elif self.subject:
            return float(self.subject.subject_coefficient)
        else:
            return 1.0  # Mặc định
    
    @property
    def effective_hourly_rate(self):
        """Tiền dạy một tiết hiệu lực (ưu tiên override, nếu không thì lấy từ teacher)"""
        if self.hourly_rate_override:
            return float(self.hourly_rate_override)
        elif self.teacher:
            return float(self.teacher.hourly_rate)
        else:
            return 100000  # Mặc định
    
    @property
    def class_coefficient(self):
        """Hệ số lớp dựa trên số sinh viên thực tế của lớp"""
        student_count = self.class_student_count or 0
        if student_count < 20:
            return -0.3
        elif 20 <= student_count <= 29:
            return -0.2
        elif 30 <= student_count <= 39:
            return -0.1
        elif 40 <= student_count <= 49:
            return 0.0
        elif 50 <= student_count <= 59:
            return 0.1
        elif 60 <= student_count <= 69:
            return 0.2
        elif 70 <= student_count <= 79:
            return 0.3
        else:  # >= 80
            return 0.4
    
    @property
    def calculated_adjusted_hours(self):
        """Tính số tiết quy đổi: Số tiết thực tế * (hệ số học phần + hệ số lớp)"""
        actual_hours = self.actual_hours or 0
        subject_coeff = self.effective_subject_coefficient
        class_coeff = self.class_coefficient
        
        return actual_hours * (subject_coeff + class_coeff)
    
    @property
    def calculated_amount(self):
        """Tính tiền dạy: Số tiết quy đổi * hệ số giáo viên * tiền dạy một tiết"""
        adjusted_hours = self.calculated_adjusted_hours
        teacher_coeff = self.effective_teacher_coefficient
        hourly_rate = self.effective_hourly_rate
        
        return adjusted_hours * teacher_coeff * hourly_rate
    
    @property
    def completion_rate(self):
        """Tỷ lệ hoàn thành giảng dạy"""
        if self.planned_hours == 0:
            return 0
        return (self.actual_hours / self.planned_hours) * 100
    
    def calculate_payment(self):
        """Tính toán và cập nhật số tiết quy đổi và tổng tiền"""
        self.adjusted_hours = self.calculated_adjusted_hours
        self.total_amount = self.calculated_amount
        return self.total_amount

    def to_dict(self):
        base_dict = super().to_dict()
        assignment_dict = {
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
            'teacher_name': self.teacher.name if self.teacher else 'N/A',
            'teacher_department': self.teacher.department if self.teacher else 'N/A',
            'subject_name': self.subject.name if self.subject else 'N/A',
            'subject_department': self.subject.department if self.subject else 'N/A',
            'semester_name': self.semester.name if self.semester else 'N/A',
            'semester_year': self.semester.year if self.semester else None,
            
            # Effective values
            'effective_teacher_coefficient': self.effective_teacher_coefficient,
            'effective_subject_coefficient': self.effective_subject_coefficient,
            'effective_hourly_rate': self.effective_hourly_rate,
            
            # Override values
            'teacher_coefficient_override': float(self.teacher_coefficient_override) if self.teacher_coefficient_override else None,
            'subject_coefficient_override': float(self.subject_coefficient_override) if self.subject_coefficient_override else None,
            'hourly_rate_override': float(self.hourly_rate_override) if self.hourly_rate_override else None,
            
            # Kết quả tính toán
            'adjusted_hours': float(self.adjusted_hours) if self.adjusted_hours else 0,
            'calculated_adjusted_hours': self.calculated_adjusted_hours,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'calculated_amount': self.calculated_amount,
            'completion_rate': round(self.completion_rate, 2),
            'class_coefficient': self.class_coefficient,
            
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'notes': self.notes,
            'is_approved': self.is_approved,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None
        }
        return {**base_dict, **assignment_dict}

    def __repr__(self):
        return f"<TeachingAssignment(teacher='{self.teacher.name if self.teacher else 'N/A'}', subject='{self.subject.name if self.subject else 'N/A'}', class='{self.class_code}')>"