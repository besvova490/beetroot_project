from app import app, db
from app.models import User, Subject
from flask import jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
import requests

jwt = JWTManager(app)


class UserConf:

    @staticmethod
    def get_user_object(user_id):
        user = User.query.get(user_id)
        if not user:
            raise KeyError(f'Unknown user with id: {user_id}')
        return user

    @staticmethod
    def check_telegram(data):
        user = User.query.filter_by(telegram_id=str(data['telegram_id'])).first()
        if user:
            return jsonify({'message': 'Old user', 'exist': True}), 200
        return jsonify({'message': 'New user', 'exist': False}), 200

    @staticmethod
    def get_users_list(is_teacher=True):
        return [user.to_dict() for user in User.query.filter_by(is_teacher=is_teacher)]

    @staticmethod
    def get_user_info(user):
        user_data = user.to_dict()
        return user_data

    @staticmethod
    def sign_up(data):
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': f'User with current email {data["email"]} exists'}), 409
        user = User(email=data['email'], password=data['password'])
        user.is_teacher = data['teacher']
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': f'{"Teacher" if data["teacher"] else "Student"} created!'}), 201

    @staticmethod
    def sign_in(data):
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return {
                'message': f"User with the following email:"
                           f" {data['email']} does not exist"
            }, 404
        if user.check_password_hash(data['password']):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            resp = jsonify({'login': True})
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp, 200
        return {'message': 'Invalid password'}, 403

    @staticmethod
    def sign_up_telegram(data):
        user = User(telegram_id=data['telegram_id'])
        user.is_teacher = data['teacher']
        user.full_name = f"{data.get('first_name', '')} {data.get('last_name', '')}"
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': f'{"Teacher" if data["teacher"] else "Student"} created!'}), 201

    @staticmethod
    def sign_in_telegram(data):
        user = User.query.filter_by(telegram_id=str(data['telegram_id'])).first()
        if not user:
            return UserConf.sign_up_telegram(data)
        resp = jsonify({'message': 'you are in sustem', 'data': UserConf.get_user_info(user)})
        return resp, 200

    @staticmethod
    def log_out():
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return resp, 200

    @staticmethod
    def update_user(user_id, data):
        user = UserConf.get_user_object(user_id)
        user.telegram_id = data.get('telegram_id', user.telegram_id)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.full_name = data.get('full_name', user.full_name)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Updated successful'}), 201

    @staticmethod
    def user_delete(user_id):
        user = UserConf.get_user_object(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 201

    @staticmethod
    def add_to_subject(user_id, subject_id):
        subject = Subject.query.get(subject_id)
        user = UserConf.get_user_object(user_id)
        if not subject:
            return jsonify({'message': 'Unknown subject'}), 404
        if user in subject.users:
            return jsonify({'message': 'User already in subject'}), 409
        subject.users.append(user)
        db.session.add(subject)
        db.session.commit()
        return jsonify({'message': 'Subject added'}), 201

    @staticmethod
    def connect_teacher_with_student(teacher_id, student_id):
        teacher = UserConf.get_user_object(teacher_id)
        student = UserConf.get_user_object(student_id)
        if not teacher or not student:
            return jsonify({'message': 'Unknown teacher or student'}), 404
        if teacher in student.teachers:
            return jsonify({'message': 'Student is already assigned to this teacher'}), 409
        student.teachers.append(teacher)
        db.session.add(student)
        db.session.commit()
        return jsonify({'message': 'Unification successful'}), 201

    @staticmethod
    def wait_for_confirmation(user_id):
        user = UserConf.get_user_object(user_id)
        scheduling = [schedule.to_dict() for schedule in user.lesson_date if not schedule.confirmation]
        return jsonify({'data': scheduling})

    @staticmethod
    def send_message(chat_id, text):
        if not chat_id:
            return {'message': 'No telegram id'}
        method = "sendMessage"
        token = "1317578331:AAEuCDPqvBDHMA68aWVuD5KdBAE92joNAqw"
        url = f"https://api.telegram.org/bot{token}/{method}"
        data = {"chat_id": chat_id, "text": text}
        requests.post(url, data=data)