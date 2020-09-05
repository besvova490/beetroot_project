from app import db

association_teachers_students = db.Table('teachers_mtm',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True)
)
association_student_subject = db.Table('students_mtm',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
)
association_teachers_subject = db.Table('subjects_mtm',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True),
    db.Column('subjects_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
)


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String())
    email = db.Column(db.String())
    phone_number = db.Column(db.String())
    full_name = db.Column(db.String())
    lesson_time_id = db.Column(db.Integer, db.ForeignKey('schedulings.id'))
    lesson_time = db.relationship("Scheduling", back_populates="teacher")
    students = db.relationship(
        "Student", secondary=association_teachers_students,
        lazy="dynamic", backref=db.backref("teachers", lazy=True)
    )
    subjects = db.relationship(
        "Subject", secondary=association_teachers_subject,
        lazy="dynamic", backref=db.backref("teachers", lazy=True)
    )

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
    lesson_time_id = db.Column(db.Integer, db.ForeignKey('schedulings.id'))
    lesson_time = db.relationship("Scheduling", back_populates="student")
    subjects = db.relationship(
        "Subject", secondary=association_student_subject,
        lazy="dynamic", backref=db.backref("students", lazy=True)
    )

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
    lesson_time_id = db.Column(db.Integer, db.ForeignKey('schedulings.id'))
    lesson_time = db.relationship("Scheduling", back_populates="subject")

    def __init__(self, title: str) -> None:
        self.title = title.title()

    def __repr__(self) -> str:
        return f'<Subject {self.title}>'


class Scheduling(db.Model):
    __tablename__ = 'schedulings'

    id = db.Column(db.Integer, primary_key=True)
    lesson_time = db.Column(db.DateTime)
    teacher = db.relationship("Teacher", back_populates="lesson_time", uselist=False)
    student = db.relationship("Student", back_populates="lesson_time", uselist=False)
    subject = db.relationship("Subject", back_populates="lesson_time", uselist=False)

    def __repr__(self) -> str:
        return f'Scheduling {self.lesson_time}'
