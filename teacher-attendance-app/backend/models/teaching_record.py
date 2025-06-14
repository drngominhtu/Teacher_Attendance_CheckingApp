from database import db
from models.base import BaseModel

class TeachingRecord(BaseModel):
    __tablename__ = 'teaching_records'
    
    assignment_id = db.Column(db.Integer, db.ForeignKey('teaching_assignments.id'), nullable=False)
    teaching_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    actual_duration = db.Column(db.Integer, nullable=False)  # Thời lượng thực tế (phút)
    lesson_topic = db.Column(db.String(200))  # Chủ đề bài giảng
    teaching_method = db.Column(db.String(50))  # Phương pháp giảng dạy
    student_count = db.Column(db.Integer, default=0)  # Số lượng sinh viên tham gia
    notes = db.Column(db.Text)
    is_makeup_class = db.Column(db.Boolean, default=False)  # Có phải tiết bù không
    is_confirmed = db.Column(db.Boolean, default=False)     # Đã xác nhận chưa
    confirmed_by = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    confirmed_at = db.Column(db.DateTime)
    
    @property
    def duration_hours(self):
        """Thời lượng theo giờ"""
        return self.actual_duration / 60

    def to_dict(self):
        base_dict = super().to_dict()
        record_dict = {
            'assignment_id': self.assignment_id,
            'teaching_date': self.teaching_date.isoformat() if self.teaching_date else None,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'actual_duration': self.actual_duration,
            'duration_hours': round(self.duration_hours, 2),
            'lesson_topic': self.lesson_topic,
            'teaching_method': self.teaching_method,
            'student_count': self.student_count,
            'notes': self.notes,
            'is_makeup_class': self.is_makeup_class,
            'is_confirmed': self.is_confirmed,
            'confirmed_by': self.confirmed_by,
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None
        }
        return {**base_dict, **record_dict}