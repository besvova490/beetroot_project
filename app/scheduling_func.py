from app import db
from app.models import Scheduling, User, Subject
from flask import jsonify
from app import users_func


class SchedulingConf:
    @staticmethod
    def get_scheduling(scheduling_id):
        return Scheduling.query.get(scheduling_id).to_dict()

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
        teacher = users_func.UserConf.get_user_object(user_id)
        if teacher in scheduling.users:
            teacher = teacher.full_name
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
        return jsonify({'msg': 'This user can not approved this schedule'}), 200

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
