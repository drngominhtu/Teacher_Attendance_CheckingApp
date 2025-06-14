from sqlalchemy import Column, Integer, String
from backend.database import Base

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)

    def __repr__(self):
        return f"<Subject(id={self.id}, name='{self.name}', department='{self.department}')>"

    @classmethod
    def create(cls, session, name, department):
        new_subject = cls(name=name, department=department)
        session.add(new_subject)
        session.commit()
        return new_subject

    @classmethod
    def update(cls, session, subject_id, name=None, department=None):
        subject = session.query(cls).filter_by(id=subject_id).first()
        if subject:
            if name:
                subject.name = name
            if department:
                subject.department = department
            session.commit()
        return subject

    @classmethod
    def delete(cls, session, subject_id):
        subject = session.query(cls).filter_by(id=subject_id).first()
        if subject:
            session.delete(subject)
            session.commit()
            return True
        return False