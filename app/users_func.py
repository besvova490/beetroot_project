from app import app, db
from app.models import User, Subject
from flask import jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
jwt = JWTManager(app)


class UserConf:

    @staticmethod
    def get_users_list(is_teacher=True):
        user_list = []
        for user in User.query.filter_by(is_teacher=is_teacher):
            users_role = {'students': tuple({'name': student.full_name, 'email': student.email} for student in user.students)}
            if not is_teacher:
                users_role = {'teachers': tuple({'name': teacher.full_name, 'email': teacher.email} for teacher in user.teachers)}
            user_list.append({
                'name': user.full_name,
                'email': user.email,
                'subjects': tuple({'name': subject.title, 'id': subject.id} for subject in user.subjects),
                **users_role
            })
        return user_list

    @staticmethod
    def get_user_dy_id(user_id):
        if not User.query.get(user_id):
            return jsonify({'message': f'Unknown user with id: {user_id}'}), 404
        user = User.query.get(user_id)
        if user.is_teacher:
            users_role = {'students': tuple({'name': student.full_name, 'email': student.email} for student in user.students)}
        else:
            users_role = {'students': tuple({'name': teacher.full_name, 'email': teacher.email} for teacher in user.teachers)}
        user_data = {
            'name': user.full_name,
            'email': user.email,
            'subjects': tuple({'name': subject.title, 'id': subject.id} for subject in user.subjects),
            **users_role
        }
        return jsonify({'data': user_data}), 200

    @staticmethod
    def sign_up(email, password, teacher):
        if User.query.filter_by(email=email).first():
            return jsonify({'message': f'User with current email {email} exists'}), 409
        user = User(email, password)
        user.is_teacher = bool(teacher)
        db.session.add(teacher)
        db.session.commit()
        return jsonify({'message': f'{"Teacher" if teacher else "Student"} created!'}), 201

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
    def log_out():
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return resp, 200

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'Unknown user'}), 404
        user.telegram_id = data.get('telegram_id', user.telegram_id)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.full_name = data.get('full_name', user.full_name)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Updated successful'}), 201

    @staticmethod
    def user_delete(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': f'Unknown user with id {user_id}'}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 201

    @staticmethod
    def add_to_subject(user_id, subject_id):
        subject = Subject.query.get(subject_id)
        user = User.query.get(user_id)
        if not user or not subject:
            return jsonify({'message': 'Unknown user or subject'}), 404
        if user in subject.teachers:
            return jsonify({'message': 'User already in subject'}), 409
        subject.user.append(user)
        db.session.add(subject)
        db.session.commit()
        return jsonify({'message': 'User added'}), 201

    @staticmethod
    def connect_teacher_with_student(teacher_id, student_id):
        teacher = User.query.get(teacher_id)
        student = User.query.get(student_id)
        if not teacher or not student:
            return jsonify({'message': 'Unknown teacher or student'}), 404
        if teacher in student.teachers:
            return jsonify({'message': 'Student is already assigned to this teacher'}), 409
        student.teachers.append(teacher)
        db.session.add(student)
        db.session.commit()
        return jsonify({'message': 'Unification successful'}), 201
