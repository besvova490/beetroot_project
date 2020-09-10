from app import db
from app.models import Scheduling, User, Subject
from flask import jsonify


class SchedulingConf:

    @staticmethod
    def add_scheduling(teacher_id, student_id, subject_id, data):
        teacher = User.query.get(int(teacher_id))
        student = User.query.get(int(student_id))
        subject = Subject.query.get(int(subject_id))
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
    def scheduling_confirmation(scheduling_id):
        scheduling = Scheduling.query.get(scheduling_id)
        student = [user.telegram_id for user in scheduling.users if not user.is_teacher]
        scheduling.confirmation = True
        db.session.add(scheduling)
        db.session.commit()
        return jsonify({'message': 'Teacher approved the lesson',
                        'status': True, 'student': student,
                        'subject': scheduling.subject.title,
                        'time': scheduling.lesson_time}), 200
