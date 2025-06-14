from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Semester(Base):
    __tablename__ = 'semesters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    subjects = relationship('Subject', secondary='semester_subject', back_populates='semesters')

    def __init__(self, name, year):
        self.name = name
        self.year = year

    def add_subject(self, subject):
        if subject not in self.subjects:
            self.subjects.append(subject)

    def remove_subject(self, subject):
        if subject in self.subjects:
            self.subjects.remove(subject)

    def __repr__(self):
        return f"<Semester(name='{self.name}', year={self.year})>"