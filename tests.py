import os
import unittest
from app import create_app, db
from app.models import User, Subject, Scheduling
from app import models_conf_classes
from config import Config, basedir
from datetime import datetime
from sqlalchemy.exc import IntegrityError


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    ELASTICSEARCH_URL = None


class FlaskTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    def setUp(self):
        User.query.delete()
        Subject.query.delete()
        Scheduling.query.delete()
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        os.remove('test.db')

    def test_is_teacher_default_false(self):
        teacher = User(email='test_teacher@gmail.com', password='test')
        student = User(email='test_student@gmail.com', password='test')
        teacher.is_teacher = True
        db.session.add(teacher)
        db.session.add(student)
        db.session.commit()
        self.assertTrue(teacher.is_teacher)
        self.assertFalse(student.is_teacher)

    def test_email(self):
        db.session.add(User(email='test_user@gmail.com'))
        db.session.commit()
        user = User(email='test_user@gmail.com')
        db.session.add(user)
        with self.app.app_context():
            self.assertRaises(IntegrityError, db.session.commit)
            self.assertIsInstance(user.email, str)

    def test_password_hashing(self):
        u = User(email='test_user@gmail.com', password='test')
        self.assertTrue(u.check_password_hash('test'))
        self.assertFalse(u.check_password_hash('Test'))

    def test_follow_to_teacher(self):
        teacher = User(email='test_teacher@gmail.com', password='test')
        student = User(email='test_student@gmail.com', password='test')
        teacher.is_teacher = True
        student.is_teacher = False
        db.session.add(teacher)
        db.session.add(student)
        db.session.commit()
        self.assertEqual(list(teacher.students), [])
        self.assertEqual(list(student.teachers), [])
        models_conf_classes.UserConf.connect_teacher_with_student(
            teacher.id, student.id
        )
        self.assertTrue(student in teacher.students)
        self.assertTrue(teacher in student.teachers)

    def test_create_subject_with_same_name(self):
        db.session.add(Subject('Test'))
        db.session.commit()
        s = Subject('Test')
        db.session.add(s)
        with self.app.app_context():
            self.assertRaises(IntegrityError, db.session.commit)

    def test_follow_subject_by_user(self):
        user = User(email='test_user@gmail.com', password='test')
        subject = Subject('Test')
        db.session.add(user)
        db.session.add(subject)
        db.session.commit()
        self.assertEqual(list(user.subjects), [])
        self.assertEqual(list(subject.users), [])
        models_conf_classes.UserConf.add_to_subject(user.id, subject.id)
        self.assertTrue(subject in user.subjects)
        self.assertTrue(user in subject.users)

    def test_scheduling_creating(self):
        teacher = User(email='test_teacher@gmail.com')
        student = User(email='test_student@gmail.com')
        subject = Subject("Test")
        teacher.is_teacher = True
        student.is_teacher = False
        db.session.add(teacher)
        db.session.add(student)
        db.session.add(subject)
        db.session.commit()
        self.assertEqual(Scheduling.query.all(), [])
        resp = models_conf_classes.SchedulingConf.add_scheduling(
            subject_id=subject.id, data=datetime.now(), users=[teacher.id, student.id]
        )
        self.assertEqual(resp[1], 201)
        sch = Scheduling.query.first()
        self.assertEqual(sch.id, 1)
        self.assertEqual(sch.subject_id, subject.id)
        self.assertTrue(teacher in sch.users)
        self.assertTrue(student in sch.users)
        self.assertTrue(sch in teacher.lesson_date)
        self.assertTrue(sch in student.lesson_date)

    def test_to_dict_method(self):
        teacher = User(email='test_teacher@gmail.com')
        subject = Subject("Test")
        teacher.is_teacher = True
        db.session.add(teacher)
        db.session.add(subject)
        db.session.commit()
        db.session.commit()
        tch_dict = teacher.to_dict()
        sub_dict = subject.to_dict()
        self.assertIsInstance(tch_dict, dict)
        self.assertIsInstance(sub_dict, dict)

    def test_get_user_object_func(self):
        user = User(email='test_user@gmail.com', password='test')
        db.session.add(user)
        db.session.commit()
        user_obj = models_conf_classes.UserConf.get_obj(User ,user.id)
        self.assertIsInstance(user_obj, User)
        self.assertEqual(user, user_obj)

    def test_get_users_list_func(self):
        teacher = User(email='test_teacher@gmail.com')
        student = User(email='test_student@gmail.com')
        teacher.is_teacher = True
        student.is_teacher = False
        db.session.add(teacher)
        db.session.add(student)
        db.session.commit()
        teachers_list = models_conf_classes.UserConf.get_objects_dict_list_or_404(User, is_teacher=True)[0].json['items']
        students_list = models_conf_classes.UserConf.get_objects_dict_list_or_404(User, is_teacher=False)[0].json['items']
        self.assertIsInstance(teachers_list, list)
        self.assertTrue(teacher.to_dict() in teachers_list)
        self.assertTrue(student.to_dict() in students_list)

    def test_update_user(self):
        user = User(email='test_user@gmail.com', password='test')
        db.session.add(user)
        db.session.commit()
        user_data = {
            'phone_number': '1234567890',
            'full_name': 'Test Name'
        }
        update = models_conf_classes.UserConf.update_obj(User, user.id, db, user_data)
        self.assertEqual(update[1], 201)
        self.assertEqual(user.phone_number, user_data['phone_number'])
        self.assertEqual(user.full_name, user_data['full_name'])

    def test_user_delete(self):
        user = User(email='test_user@gmail.com', password='test')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.first(), user)
        resp = models_conf_classes.UserConf.delete_object(user, db)
        self.assertEqual(resp[1], 201)
        self.assertEqual(User.query.first(), None)

    def test_get_subjects_list(self):
        subject_list_empty = models_conf_classes.SubjectConf.get_objects_dict_list_or_404(Subject)[0].json
        subject = Subject('Test')
        db.session.add(subject)
        db.session.commit()
        subject_list = models_conf_classes.SubjectConf.get_objects_dict_list_or_404(Subject)[0].json
        self.assertTrue(subject.to_dict() in subject_list['items'])
        self.assertEqual(subject_list_empty['msg'], 'objects is not found')
        self.assertEqual(subject_list_empty.get('items', False), False)

    def test_get_subject_by_id_func(self):
        subject = Subject('Test')
        db.session.add(subject)
        db.session.commit()
        subject_data = models_conf_classes.SubjectConf.get_obj_dict_or_404(Subject, subject.id)
        self.assertEqual(subject.to_dict(), subject_data[0].json['item'])

    def test_create_subject_func(self):
        subject_data = {'title': 'Test'}
        resp = models_conf_classes.SubjectConf.create_subject(subject_data)
        subject = Subject.query.filter_by(title=subject_data['title']).first()
        self.assertEqual(resp[1], 201)
        self.assertEqual(subject.title, subject_data['title'])
        self.assertIsInstance(subject, Subject)

    def test_subject_update(self):
        subject = Subject('Test')
        db.session.add(subject)
        db.session.commit()
        subject_data = {'description': 'Test description'}
        update = models_conf_classes.SubjectConf.update_obj(Subject, subject.id, db, subject_data)
        self.assertEqual(update[1], 201)
        self.assertEqual(subject.description, subject_data['description'])

    def test_subject_delete(self):
        subject = Subject('Test')
        db.session.add(subject)
        db.session.commit()
        self.assertEqual(Subject.query.get(subject.id), subject)
        deleted = models_conf_classes.SubjectConf.delete_object(subject, db)
        self.assertEqual(deleted[1], 201)
        self.assertEqual(Subject.query.get(subject.id), None)


if __name__ == '__main__':
    unittest.main(verbosity=2)
