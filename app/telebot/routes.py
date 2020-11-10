from app import db, email
from app.telebot import bp
from app.models_conf_classes import UserConf, SubjectConf, SchedulingConf
from app.models import User, Subject, Scheduling
from flask import jsonify, request
import datetime
import os

@bp.route('/users', methods=['GET'])
def users_page():
    return UserConf.get_objects_dict_list_or_404(User, **request.args)


@bp.route('/subjects', methods=['GET'])
def subjects():
    return SubjectConf.get_objects_dict_list_or_404(Subject)


@bp.route('/users/<int:user_id>', methods=['GET'])
def user_page(user_id):
    query = request.args
    if query and query['action'] == 'follow_user':
        resp = UserConf.connect_teacher_with_student(user_id, query['user_id'])
        return resp
    if query and query['action'] == 'follow_subject':
        resp = UserConf.add_to_subject(user_id, query['subject_id'])
        return resp
    if query and query['action'] == 'get_schedule':
        resp = UserConf.get_user_schedule(user_id, status=True if query['approved'] == 'True' else False)
        return resp
    return UserConf.get_obj_dict_or_404(User, user_id)


@bp.route('/subjects', methods=['POST'])
def subject_create():
    subject_data = request.json['data']
    return SubjectConf.create_subject(subject_data)


@bp.route('/subjects/<int:subject_id>', methods=['DELETE'])
def subject_delete(subject_id):
    subject = SubjectConf.get_obj(Subject, subject_id)
    return SubjectConf.delete_object(subject, db)


@bp.route('/subjects/<int:subject_id>', methods=['GET'])
def subject_page(subject_id):
    return SubjectConf.get_obj_dict_or_404(Subject, subject_id)


@bp.route('/schedule/', methods=['POST'])
def add_scheduling():
    data = request.json['data']
    data['lesson_time'] = datetime.datetime.strptime(data['lesson_time'], '%Y-%m-%dT%H:%M:%SZ')
    resp = SchedulingConf.add_scheduling(
        data['subject'], data['lesson_time'], data['users']
    )
    return resp


@bp.route('/schedule/<int:scheduling_id>', methods=['GET'])
def scheduling_confirmation(scheduling_id):
    query = request.args
    if query:
        if query['set_conformation'] == 'Flase':
            return SchedulingConf.delete_scheduling(scheduling_id)
        return SchedulingConf.scheduling_confirmation(scheduling_id, user_id=query['user_id'])
    return SchedulingConf.get_obj_dict_or_404(Scheduling, scheduling_id)


@bp.route('/schedule/<int:scheduling_id>', methods=['DELETE'])
def delete_scheduling(scheduling_id):
    return SchedulingConf.delete_scheduling(scheduling_id)


@bp.route('/telegram-sign-up', methods=['POST'])
def user_create_telegram():
    user_data = request.json['data']
    return UserConf.sign_up_telegram(user_data)


@bp.route('/telegram-sign-in', methods=['POST'])
def user_sign_in_telegram():
    user_data = request.json['data']
    return UserConf.sign_in_telegram(user_data)


@bp.route('/export-schedule', methods=['POST'])
def get_schedule_in_excel():
    email.send_email('test', os.environ.get('MAIL_USERNAME'), ['besvova490@gmail.com'], 'Test')
    resp = request.json['data']
    user = UserConf.get_obj(User, resp['user_id'])
    user.launch_task('export_posts', 'Exporting posts...')
    db.session.commit()
    return jsonify({'msg': 'Schedule sanded to your email'}), 200
