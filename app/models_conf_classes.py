from app import db, base_func
from app.models import User, Subject, Scheduling
from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
import requests


class UserConf(base_func.BaseFuncs):

    @staticmethod
    def sign_up(data):
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'msg': f'User with current email {data["email"]} exists'
            }), 409
        user = User(**data)
        user.is_teacher = data.get('is_teacher', False)
        db.session.add(user)
        db.session.commit()
        return jsonify({'msg': f'{"Teacher" if user.is_teacher else "Student"}'
                               f' created', 'item_id': user.id}), 201

    @staticmethod
    def sign_in(data):
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return {
                'msg': f"User with the following email:"
                       f" {data['email']} does not found"
            }, 404
        if user.check_password_hash(data['password']):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            resp = jsonify({'login': True, 'item_id': user.id})
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp, 200
        return {'msg': 'Invalid password'}, 401

    @staticmethod
    def sign_up_telegram(data):
        if User.query.filter_by(telegram_id=data['telegram_id']).first():
            return jsonify({'msg': 'User exist'}), 409
        user = User(telegram_id=data['telegram_id'])
        user.is_teacher = data.get('teacher', False)
        user.email = data.get('email', '')
        user.full_name = f"{data.get('first_name', '')}" \
                         f" {data.get('last_name', '')}".strip()
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'msg': f'{"Teacher" if user.is_teacher else "Student"} created!'
        }), 201

    @staticmethod
    def sign_in_telegram(data):
        user = User.query.filter_by(telegram_id=data['telegram_id']).first()
        if not user:
            return jsonify({'massage': 'User not exist'}), 401
        resp = jsonify({'msg': 'You are in Authorized',
                        'items': user.to_dict()})
        return resp, 200

    @staticmethod
    def log_out():
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return resp, 200

    @staticmethod
    def add_to_subject(user_id, subject_id):
        subject = Subject.query.get(subject_id)
        user = UserConf.get_obj(User, user_id)
        if not subject:
            return jsonify({'msg': 'Unknown subject'}), 401
        if user in subject.users:
            return jsonify({'msg': 'User already in subject'}), 409
        subject.users.append(user)
        db.session.add(subject)
        db.session.commit()
        return jsonify({'msg': 'Subject added'}), 201

    @staticmethod
    def connect_teacher_with_student(user1_id, user2_id):
        user1 = UserConf.get_obj(User, user1_id)
        user2 = UserConf.get_obj(User, user2_id)
        if not user1 or not user2:
            return jsonify({'msg': 'Unknown teacher or student'}), 401
        if user2.is_teacher:
            if user1 in user2.teachers:
                return jsonify({
                    'msg': 'Student is already assigned to this teacher'
                }), 409
            user1.teachers.append(user2)
        else:
            if user2 in user1.teachers:
                return jsonify({
                    'msg': 'Student is already assigned to this teacher'
                }), 409
            user2.teachers.append(user1)
        db.session.commit()
        return jsonify({'msg': 'Unification successful'}), 201

    @staticmethod
    def get_user_schedule(user_id, status=True):
        user = UserConf.get_obj(User, user_id)
        scheduling = [schedule.to_dict() for schedule in user.lesson_date if schedule.confirmation == status]
        if scheduling:
            return jsonify({
                'msg': 'Subjects that wait for approved', 'items': scheduling
            }), 200
        return jsonify({'msg': 'Now schedules for this user'}), 204

    @staticmethod
    def send_message(chat_id, text):
        method = "sendMessage"
        token = "1317578331:AAEuCDPqvBDHMA68aWVuD5KdBAE92joNAqw"
        url = f"https://api.telegram.org/bot{token}/{method}"
        data = {"chat_id": chat_id, "text": text}
        requests.post(url, data=data)


class SubjectConf(base_func.BaseFuncs):

    @staticmethod
    def create_subject(data):
        if not data['title']:
            return jsonify({'msg': 'Can not create subject with empty title'}), 400
        if Subject.query.filter_by(title=data['title']).first():
            return jsonify({'msg': f'Subject with current title {data["title"]} exists'}), 409
        subject = Subject(**data)
        db.session.add(subject)
        db.session.commit()
        return jsonify({'msg': f'Subject crested', 'item_id': subject.id}), 201


class SchedulingConf(base_func.BaseFuncs):

    @staticmethod
    def add_scheduling(subject_id, data, users):
        user1 = User.query.get(users[0])
        user2 = User.query.get(users[1])
        subject = Subject.query.get(subject_id)
        if not user1 or not user2:
            return jsonify({'message': 'Wrong data for student or teacher'}), 400
        if not subject:
            return jsonify({'message': 'Wrong data for subject'}), 400
        scheduling = Scheduling()
        scheduling.lesson_time = data
        scheduling.users.append(user1)
        scheduling.users.append(user2)
        scheduling.subject = subject
        db.session.add(scheduling)
        db.session.commit()

        return jsonify({'message': 'Scheduling is created', 'data': scheduling.lesson_time}), 201

    @staticmethod
    def teacher_scheduling(scheduling):
        for user in scheduling.users:
            if user.is_teacher:
                return {'id': user.id, 'name': user.full_name}

    @staticmethod
    def student_scheduling(scheduling):
        for user in scheduling.users:
            if not user.is_teacher:
                return {'id': user.id, 'name': user.full_name}

    @staticmethod
    def scheduling_confirmation(scheduling_id, user_id):
        scheduling = Scheduling.query.get(scheduling_id)
        students = [user.telegram_id for user in scheduling.users if not user.is_teacher and user.telegram_id]
        teacher = UserConf.get_obj(User, user_id)
        if teacher in scheduling.users:
            teacher = teacher.full_name
            scheduling.confirmation = True
            db.session.commit()
            resp = jsonify({'message': 'Teacher approved the lesson',
                            'status': True, 'subject': scheduling.subject.title,
                            'time': scheduling.lesson_time}), 200
            if not students:
                return resp
            for student in students:
                message = f'Teacher: {teacher} approved lesson: ' \
                          f'{scheduling.subject.title} \nLesson time: {scheduling.lesson_time}'
                UserConf.send_message(student, message)
            return resp
        return jsonify({'msg': 'This user can not approved this schedule'}), 200

    @staticmethod
    def delete_scheduling(scheduling_id):
        scheduling = Scheduling.query.get(scheduling_id)
        if not scheduling:
            return jsonify({'message': 'Unknown scheduling'}), 409
        students = [user.telegram_id for user in scheduling.users if not user.is_teacher and user.telegram_id]
        if students:
            for student in students:
                message = f'Teacher rejected lesson: ' \
                          f'{scheduling.subject.title} \nLesson time: {scheduling.lesson_time}'
                UserConf.send_message(student, message)
        db.session.delete(scheduling)
        db.session.commit()
        return jsonify({'message': 'Scheduling deleted'}), 201
