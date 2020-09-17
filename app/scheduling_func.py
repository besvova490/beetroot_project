from app import db
from app.models import Scheduling, User, Subject
from flask import jsonify
from app import users_func


class SchedulingConf:

    @staticmethod
    def add_scheduling(teacher_id, student_id, subject_id, data):
        teacher = User.query.get(teacher_id)
        student = User.query.get(student_id)
        subject = Subject.query.get(subject_id)
        if not teacher:
            return jsonify({'message': 'Wrong data for teacher'}), 404
        if not student:
            return jsonify({'message': 'Wrong data for student'}), 404
        if not subject:
            return jsonify({'message': 'Wrong data for subject'}), 404
        scheduling = Scheduling()
        scheduling.lesson_time = data
        scheduling.users.append(teacher)
        scheduling.users.append(student)
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
        teacher = users_func.UserConf.get_user_object(user_id).full_name
        scheduling.confirmation = True
        db.session.add(scheduling)
        db.session.commit()
        resp = jsonify({'message': 'Teacher approved the lesson',
                        'status': True, 'subject': scheduling.subject.title,
                        'time': scheduling.lesson_time}), 200
        if not students:
            return resp
        for student in students:
            message = f'Teacher: {teacher} approved lesson: ' \
                      f'{scheduling.subject.title} \nLesson time: {scheduling.lesson_time}'
            users_func.UserConf.send_message(student, message)
        return resp

    @staticmethod
    def delete_scheduling(scheduling_id):
        scheduling = Scheduling.query.get(scheduling_id)
        if not scheduling:
            return jsonify({'message': 'Unknown scheduling'}), 409
        students = [user.telegram_id for user in scheduling.users if
                   not user.is_teacher and user.telegram_id]
        if students:
            for student in students:
                message = f'Teacher rejected lesson: ' \
                          f'{scheduling.subject.title} \nLesson time: {scheduling.lesson_time}'
                users_func.UserConf.send_message(student, message)
        db.session.delete(scheduling)
        db.session.commit()
        return jsonify({'message': 'Scheduling deleted'}), 201
