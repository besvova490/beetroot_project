from app import db
from passlib.hash import sha256_crypt


association_users_roles = db.Table(
    'association_users_roles',
    db.Column('student_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('teacher_id', db.Integer, db.ForeignKey('users.id'))
)
association_users_subject = db.Table('subjects_mtm',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('subjects_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
)
association_users_scheduling = db.Table('users_scheduling_mtm',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('scheduling_id', db.Integer, db.ForeignKey('schedulings.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String(128))
    phone_number = db.Column(db.String())
    full_name = db.Column(db.String())
    is_teacher = db.Column(db.Boolean, default=False)
    lesson_date = db.relationship(
        "Scheduling", secondary=association_users_scheduling,
        lazy="dynamic", backref=db.backref("users", lazy=True)
    )
    teachers = db.relationship(
        'User', secondary=association_users_roles,
        primaryjoin=(association_users_roles.c.teacher_id == id),
        secondaryjoin=(association_users_roles.c.student_id == id),
        backref=db.backref('students', lazy='dynamic'), lazy='dynamic')
    subjects = db.relationship(
        "Subject", secondary=association_users_subject,
        lazy="dynamic", backref=db.backref("users", lazy=True)
    )

    def check_password_hash(self, password):
        return sha256_crypt.verify(password, self.password)

    def __init__(self, email=None, password='', telegram_id=None) -> None:
        self.email = email
        self.password = sha256_crypt.hash(password.strip())
        self.telegram_id = telegram_id

    def to_dict(self):
        if self.is_teacher:
            users = self.students
        else:
            users = self.teachers
        return dict(
            id=self.id, telegram_id=self.telegram_id, email=self.email,
            phone_number=self.phone_number, name=self.full_name,
            is_teacher=self.is_teacher, lesson_date=[{'id': lesson_time.id, 'time': lesson_time.lesson_time, 'confirmation': lesson_time.confirmation, 'subject': lesson_time.subject.title} for lesson_time in self.lesson_date],
            subjects=[{'id': subject.id, 'title': subject.title} for subject in self.subjects],
            users=[{'id': user.id, 'telegram_id': user.telegram_id, 'name': user.full_name, 'is_teacher': user.is_teacher, 'email': user.email} for user in users]
        )

    def __repr__(self) -> str:
        return f'<{"Teacher" if self.is_teacher else "Student"}: {self.email}>'


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String())
    lesson_time = db.relationship("Scheduling", backref="subject", lazy='dynamic', cascade="all, delete")

    def __init__(self, title: str) -> None:
        self.title = title.title()

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            lesson_time=[{'id': lesson_time.id, 'time': lesson_time.lesson_time, 'confirmation': lesson_time.confirmation, 'subject': lesson_time.subject.title} for lesson_time in self.lesson_time],
            users=[{'id': user.id, 'telegram_id': user.telegram_id, 'name': user.full_name, 'is_teacher': user.is_teacher, 'email': user.email} for user in self.users]
        )

    def __repr__(self) -> str:
        return f'<Subject: {self.title}>'


class Scheduling(db.Model):
    __tablename__ = 'schedulings'

    id = db.Column(db.Integer, primary_key=True)
    confirmation = db.Column(db.Boolean, default=False)
    lesson_time = db.Column(db.DateTime)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))

    def to_dict(self):
        return dict(
            id=self.id,
            status=self.confirmation,
            lesson_time=self.lesson_time,
            subject={'id': self.subject_id, 'title': self.subject.title},
            users=[{'id': user.id, 'telegram_id': user.telegram_id, 'name': user.full_name, 'is_teacher': user.is_teacher, 'email': user.email} for user in self.users]
        )

    def __repr__(self) -> str:
        return f'<Scheduling: {self.lesson_time}>'
