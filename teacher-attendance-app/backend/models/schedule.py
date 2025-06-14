from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from database import db
from models.base import BaseModel

class Schedule(BaseModel):
    __tablename__ = 'schedules'

    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    classroom = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        base_dict = super().to_dict()
        schedule_dict = {
            'subject_id': self.subject_id,
            'teacher_id': self.teacher_id,
            'semester_id': self.semester_id,
            'day_of_week': self.day_of_week,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'classroom': self.classroom,
            'notes': self.notes
        }
        return {**base_dict, **schedule_dict}

    def __repr__(self):
        return f"<Schedule(subject_id={self.subject_id}, teacher_id={self.teacher_id}, day='{self.day_of_week}')>"