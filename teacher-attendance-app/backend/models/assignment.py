from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Assignment(Base):
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))

    teacher = relationship("Teacher", back_populates="assignments")
    subject = relationship("Subject", back_populates="assignments")

    def __repr__(self):
        return f"<Assignment(teacher_id={self.teacher_id}, subject_id={self.subject_id})>"