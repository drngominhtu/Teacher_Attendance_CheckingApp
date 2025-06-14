from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from backend.database import Base

class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    semester_id = Column(Integer, ForeignKey('semesters.id'), nullable=False)
    day_of_week = Column(String(10), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    subject = relationship("Subject", back_populates="schedules")
    teacher = relationship("Teacher", back_populates="schedules")
    semester = relationship("Semester", back_populates="schedules")

    def __repr__(self):
        return f"<Schedule(id={self.id}, subject_id={self.subject_id}, teacher_id={self.teacher_id}, semester_id={self.semester_id}, day_of_week='{self.day_of_week}', start_time='{self.start_time}', end_time='{self.end_time}')>"