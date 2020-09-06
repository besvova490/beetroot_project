from app import db
from passlib.hash import sha256_crypt


association_users_roles = db.Table(
    'association_users_roles',
    db.Column('student_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('teacher_id', db.Integer, db.ForeignKey('users.id'))
)
association_teachers_subject = db.Table('subjects_mtm',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('subjects_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String(128))
    phone_number = db.Column(db.String())
    full_name = db.Column(db.String())
    is_teacher = db.Column(db.Boolean, default=False)
    lesson_date = db.Column(db.Integer, db.ForeignKey('schedulings.id'))
    teachers = db.relationship(
        'User', secondary=association_users_roles,
        primaryjoin=(association_users_roles.c.teacher_id == id),
        secondaryjoin=(association_users_roles.c.student_id == id),
        backref=db.backref('students', lazy='dynamic'), lazy='dynamic')
    subjects = db.relationship(
        "Subject", secondary=association_teachers_subject,
        lazy="dynamic", backref=db.backref("users", lazy=True)
    )

    def check_password_hash(self, password):
        return sha256_crypt.verify(password, self.password)

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = sha256_crypt.hash(password.strip())

    def __repr__(self) -> str:
        return f'<{"Teacher" if self.is_teacher else "Student"}: {self.email}>'


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
        return f'<Subject: {self.title}>'


class Scheduling(db.Model):
    __tablename__ = 'schedulings'

    id = db.Column(db.Integer, primary_key=True)
    lesson_time = db.Column(db.DateTime)
    users = db.relationship("User")
    subject = db.relationship("Subject", back_populates="lesson_time", uselist=False)

    def __repr__(self) -> str:
        return f'<Scheduling: {self.lesson_time}>'
