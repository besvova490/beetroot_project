from app import users_func, subject_func, scheduling_func
from app.telebot import bp
from flask import jsonify, request
import datetime


@bp.route('/tutors', methods=['GET'])
def tutors_page():
    return users_func.UserConf.get_users_list(is_teacher=True)


@bp.route('/students', methods=['GET'])
def students_page():
    return users_func.UserConf.get_users_list(is_teacher=False)


@bp.route('/subjects', methods=['GET'])
def subjects():
    resp_subjects = subject_func.SubjectConf.get_subjects_list()
    return resp_subjects


@bp.route('/user/<int:user_id>', methods=['GET'])
def user_page(user_id):
    return users_func.UserConf.get_user_info(user_id)


@bp.route('/user/<int:user_id>/scheduling/<int:scheduling_id>', methods=['POST'])
def scheduling_confirmation(user_id, scheduling_id):
    resp = scheduling_func.SchedulingConf.scheduling_confirmation(scheduling_id, user_id)
    return resp


@bp.route('/user/<int:user_id>/schedule-not-confirmed', methods=['GET'])
def schedule_confirmed(user_id):
    return users_func.UserConf.wait_for_confirmation(user_id)


@bp.route('/user/<int:teacher_id>/<int:user_id>', methods=['POST'])
def connect_user_teacher(teacher_id, user_id):
    resp = users_func.UserConf.connect_teacher_with_student(teacher_id, user_id)
    return resp


@bp.route('/subjects', methods=['POST'])
def subject_create():
    subject_data = request.json['data']
    create = subject_func.SubjectConf.create_subject(subject_data)
    return create


@bp.route('/subjects/<int:subject_id>', methods=['DELETE'])
def subject_delete(subject_id):
    resp = subject_func.SubjectConf.subject_delete(subject_id)
    return resp


@bp.route('/subjects/<int:subject_id>', methods=['GET'])
def subject_page(subject_id):
    resp = subject_func.SubjectConf.get_subject_by_id(subject_id)
    return resp


@bp.route('/subjects/<int:subject_id>/<int:user_id>', methods=['POST'])
def add_user_to_subject(user_id, subject_id):
    resp = users_func.UserConf.add_to_subject(user_id, subject_id)
    return resp


@bp.route('/scheduling', methods=['POST'])
def add_scheduling():
    data = request.json['data']
    data['time'] = datetime.datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
    resp = scheduling_func.SchedulingConf.add_scheduling(
        data['teacher'], data['student'], data['subject'], data['time']
    )
    return resp


@bp.route('/scheduling/<int:scheduling_id>', methods=['DELETE'])
def delete_scheduling(scheduling_id):
    resp = scheduling_func.SchedulingConf.delete_scheduling(scheduling_id)
    return resp


@bp.route('/telegram-sign-up', methods=['POST'])
def user_create_telegram():
    user_data = request.json['data']
    create = users_func.UserConf.sign_up_telegram(user_data)
    return create


@bp.route('/telegram-sign-in', methods=['POST'])
def user_sign_in_telegram():
    user_data = request.json['data']
    return users_func.UserConf.sign_in_telegram(user_data)
