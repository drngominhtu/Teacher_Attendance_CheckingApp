from database import db
from models.base import BaseModel

class SalaryCalculation(BaseModel):
    __tablename__ = 'salary_calculations'
    
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    calculation_period = db.Column(db.String(20), nullable=False)  # Kỳ tính lương (VD: 2024-01)
    calculation_type = db.Column(db.String(20), default='monthly')  # monthly, semester, custom
    
    # Lương cơ bản
    base_salary = db.Column(db.Numeric(12, 2), default=0)
    
    # Tiền giảng dạy
    teaching_hours = db.Column(db.Integer, default=0)       # Tổng giờ dạy
    teaching_amount = db.Column(db.Numeric(12, 2), default=0)  # Tiền giảng dạy
    
    # Phụ cấp và thưởng
    position_allowance = db.Column(db.Numeric(12, 2), default=0)    # Phụ cấp chức vụ
    research_bonus = db.Column(db.Numeric(12, 2), default=0)        # Thưởng nghiên cứu
    overtime_amount = db.Column(db.Numeric(12, 2), default=0)       # Tiền làm thêm giờ
    other_allowances = db.Column(db.Numeric(12, 2), default=0)      # Phụ cấp khác
    
    # Khấu trừ
    insurance_deduction = db.Column(db.Numeric(12, 2), default=0)   # Trừ bảo hiểm
    tax_deduction = db.Column(db.Numeric(12, 2), default=0)         # Trừ thuế
    other_deductions = db.Column(db.Numeric(12, 2), default=0)      # Trừ khác
    
    # Tổng kết
    gross_salary = db.Column(db.Numeric(12, 2), default=0)          # Tổng lương trước trừ
    net_salary = db.Column(db.Numeric(12, 2), default=0)            # Lương thực lĩnh
    
    # Trạng thái
    status = db.Column(db.String(20), default='draft')  # draft, calculated, approved, paid
    notes = db.Column(db.Text)
    calculated_by = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    calculated_at = db.Column(db.DateTime)
    approved_by = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    approved_at = db.Column(db.DateTime)
    
    def calculate_totals(self):
        """Tính toán tổng lương"""
        self.gross_salary = (
            self.base_salary + 
            self.teaching_amount + 
            self.position_allowance + 
            self.research_bonus + 
            self.overtime_amount + 
            self.other_allowances
        )
        
        total_deductions = (
            self.insurance_deduction + 
            self.tax_deduction + 
            self.other_deductions
        )
        
        self.net_salary = self.gross_salary - total_deductions

    def to_dict(self):
        base_dict = super().to_dict()
        salary_dict = {
            'teacher_id': self.teacher_id,
            'calculation_period': self.calculation_period,
            'calculation_type': self.calculation_type,
            'base_salary': float(self.base_salary) if self.base_salary else 0,
            'teaching_hours': self.teaching_hours,
            'teaching_amount': float(self.teaching_amount) if self.teaching_amount else 0,
            'position_allowance': float(self.position_allowance) if self.position_allowance else 0,
            'research_bonus': float(self.research_bonus) if self.research_bonus else 0,
            'overtime_amount': float(self.overtime_amount) if self.overtime_amount else 0,
            'other_allowances': float(self.other_allowances) if self.other_allowances else 0,
            'insurance_deduction': float(self.insurance_deduction) if self.insurance_deduction else 0,
            'tax_deduction': float(self.tax_deduction) if self.tax_deduction else 0,
            'other_deductions': float(self.other_deductions) if self.other_deductions else 0,
            'gross_salary': float(self.gross_salary) if self.gross_salary else 0,
            'net_salary': float(self.net_salary) if self.net_salary else 0,
            'status': self.status,
            'notes': self.notes,
            'calculated_by': self.calculated_by,
            'calculated_at': self.calculated_at.isoformat() if self.calculated_at else None,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None
        }
        return {**base_dict, **salary_dict}