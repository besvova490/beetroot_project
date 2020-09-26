from app import db
from app.models import Subject
from flask import jsonify


class SubjectConf:

    @staticmethod
    def get_subjects_list():
        subject_list = Subject.query.all()
        if not subject_list:
            return jsonify({'msg': 'Is now subjects yet'}), 200
        return jsonify({'msg': 'Subjects list', 'items': [subject.to_dict() for subject in subject_list]}), 200

    @staticmethod
    def get_subject_by_id(subject_id):
        if not Subject.query.get(subject_id):
            return jsonify({'msg': f'Unknown subject with id: {subject_id}'}), 400
        return jsonify({'msg': 'Subject found', 'items': Subject.query.get(subject_id).to_dict()}), 200

    @staticmethod
    def create_subject(data):
        if Subject.query.filter_by(title=data['title']).first():
            return jsonify({'msg': f'Subject with current title {data["title"]} exists'}), 409
        if not data['title'].strip():
            return jsonify({'msg': 'Can not create subject with empty title'}), 400
        subject = Subject(data['title'].strip())
        db.session.add(subject)
        db.session.commit()
        return jsonify({'msg': f'Subject crested', 'item_id': subject.id}), 201

    @staticmethod
    def subject_update(subject_id, data):
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({'msg': f'Unknown subject with id: {subject_id}'}), 401
        subject.description = data.get('description', subject.description).strip()
        db.session.add(subject)
        db.session.commit()
        return jsonify({'msg': 'Subject is updated', 'item_id': subject.id}), 201

    @staticmethod
    def subject_delete(subject_id):
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({'msg': f'Unknown subject with id: {subject_id}'}), 401
        db.session.delete(subject)
        db.session.commit()
        return jsonify({'msg': 'Subject deleted'}), 201
