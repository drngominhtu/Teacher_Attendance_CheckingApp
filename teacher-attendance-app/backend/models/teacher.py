from sqlalchemy import Column, Integer, String
from backend.database import Base

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    qualifications = Column(String, nullable=True)

    def __repr__(self):
        return f"<Teacher(id={self.id}, name='{self.name}', department='{self.department}', qualifications='{self.qualifications}')>"

    def create_teacher(self, session, name, department, qualifications):
        new_teacher = Teacher(name=name, department=department, qualifications=qualifications)
        session.add(new_teacher)
        session.commit()
        return new_teacher

    def update_teacher(self, session, teacher_id, name=None, department=None, qualifications=None):
        teacher = session.query(Teacher).filter_by(id=teacher_id).first()
        if teacher:
            if name:
                teacher.name = name
            if department:
                teacher.department = department
            if qualifications:
                teacher.qualifications = qualifications
            session.commit()
        return teacher

    def delete_teacher(self, session, teacher_id):
        teacher = session.query(Teacher).filter_by(id=teacher_id).first()
        if teacher:
            session.delete(teacher)
            session.commit()
            return True
        return False