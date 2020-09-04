from app import db


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String())
    email = db.Column(db.String())
    phone_number = db.Column(db.String())
    full_name = db.Column(db.String())
    lesson_time = db.relationship("Scheduling", back_populates="teacher")

    def __init__(self, email: str, first_name: str, last_name: str, phone_number: str) -> None:
        self.email = email.title()
        self.full_name = f'{first_name} {last_name}'.title()
        self.phone_number = phone_number

    def __repr__(self) -> str:
        return f'<Teacher {self.full_name} - {self.phone_number}>'


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String())
    email = db.Column(db.String())
    phone_number = db.Column(db.String())
    full_name = db.Column(db.String())
    lesson_time = db.relationship("Scheduling", back_populates="student")

    def __init__(self, email: str, first_name: str, last_name: str, phone_number: str) -> None:
        self.email = email.title()
        self.full_name = f'{first_name} {last_name}'.title()
        self.phone_number = phone_number

    def __repr__(self) -> str:
        return f'<Student {self.full_name} - {self.phone_number}>'


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    lesson_time = db.relationship("Scheduling", back_populates="subject")

    def __init__(self, title: str) -> None:
        self.title = title.title()

    def __repr__(self) -> str:
        return f'<Subject {self.title}>'


class Scheduling(db.Model):
    __tablename__ = 'scheduling'

    id = db.Column(db.Integer, primary_key=True)
    lesson_time = db.Column(db.DateTime)
    teacher = db.relationship("Teacher", back_populates="lesson_time")
    student = db.relationship("Student", back_populates="lesson_time")
    subject = db.relationship("Subject", back_populates="lesson_time")
