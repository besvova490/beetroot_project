from app import db
from app.models import Subject
from flask import jsonify


class SubjectConf:

    @staticmethod
    def get_subjects_list():
        subjects_list = []
        for subject in Subject.query.all():
            subjects_list.append({
                'id': subject.id,
                'title': subject.title,
                'description': subject.description,
                'teachers': tuple({'name': teacher.full_name, 'email': teacher.email} for teacher in subject.users if teacher.is_teacher),
                'students': tuple({'name': student.full_name, 'email': student.email} for student in subject.users if not student.is_teacher)
            })
        return subjects_list

    @staticmethod
    def get_subject_by_id(subject_id):
        if not Subject.query.get(subject_id):
            return jsonify({'message': f'Unknown subject with id: {subject_id}'}), 404
        subject = Subject.query.get(subject_id)
        subject_data = {
            'title': subject.title,
            'description': subject.description,
            'teachers': tuple(
                {'name': teacher.full_name, 'email': teacher.email} for teacher in
                subject.users if teacher.is_teacher),
            'students': tuple(
                {'name': student.full_name, 'email': student.email} for student in
                subject.users if not student.is_teacher)
        }
        return jsonify({'data': subject_data}), 200

    @staticmethod
    def create_subject(data):
        if Subject.query.filter_by(title=data['title']).first():
            return jsonify({'message': f'Subject with current title {data["title"]} exists'}), 409
        subject = Subject(data['title'])
        db.session.add(subject)
        db.session.commit()
        return jsonify({'message': 'Subject crested!'}), 201

    @staticmethod
    def subject_update(subject_id, data):
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({'message': f'Unknown subject with id: {subject_id}'}), 404
        subject.title = data.get('title', subject.title)
        subject.description = data.get('description', subject.description)
        db.session.add(subject)
        db.session.commit()
        return jsonify({'message': 'Subject is updated!'}), 201

    @staticmethod
    def subject_delete(subject_id):
        subject = Subject.query.get(subject_id)
        db.session.delete(subject)
        db.session.commit()
        return jsonify({'message': 'Subject deleted'}), 201
