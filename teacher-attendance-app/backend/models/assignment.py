from database import db
from models.base import BaseModel

class Assignment(BaseModel):
    __tablename__ = 'assignments'

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=True)

    def to_dict(self):
        base_dict = super().to_dict()
        assignment_dict = {
            'teacher_id': self.teacher_id,
            'subject_id': self.subject_id,
            'semester_id': self.semester_id,
        }
        return {**base_dict, **assignment_dict}

    def __repr__(self):
        return f"<Assignment(teacher_id={self.teacher_id}, subject_id={self.subject_id})>"