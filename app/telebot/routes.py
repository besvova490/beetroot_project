from app import users_func, subject_func, scheduling_func, db, email
from app.telebot import bp
from flask import jsonify, request
import datetime


@bp.route('/users', methods=['GET'])
def users_page():
    query = request.args
    return users_func.UserConf.get_users_list(is_teacher=True if query['users'] == 'teachers' else False)


@bp.route('/subjects', methods=['GET'])
def subjects():
    resp_subjects = subject_func.SubjectConf.get_subjects_list()
    return resp_subjects


@bp.route('/users/<int:user_id>', methods=['GET'])
def user_page(user_id):
    query = request.args
    if query and query['action'] == 'follow_user':
        resp = users_func.UserConf.connect_teacher_with_student(user_id, query['user_id'])
        return resp
    if query and query['action'] == 'follow_subject':
        resp = users_func.UserConf.add_to_subject(user_id, query['subject_id'])
        return resp
    if query and query['action'] == 'get_schedule':
        resp = users_func.UserConf.get_user_schedule(user_id, conformed=True if query['approved'] == 'True' else False)
        return resp
    return users_func.UserConf.get_user_info(user_id)


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


@bp.route('/schedule/', methods=['POST'])
def add_scheduling():
    data = request.json['data']
    data['lesson_time'] = datetime.datetime.strptime(data['lesson_time'], '%Y-%m-%dT%H:%M:%SZ')
    resp = scheduling_func.SchedulingConf.add_scheduling(
        data['subject'], data['lesson_time'], data['users']
    )
    return resp


@bp.route('/schedule/<int:scheduling_id>', methods=['GET'])
def scheduling_confirmation(scheduling_id):
    query = request.args
    if query:
        if query['set_conformation'] == 'Flase':
            resp = scheduling_func.SchedulingConf.delete_scheduling(scheduling_id)
            return resp
        resp = scheduling_func.SchedulingConf.scheduling_confirmation(scheduling_id, user_id=query['user_id'])
        return resp
    resp = scheduling_func.SchedulingConf.get_scheduling(scheduling_id)
    return resp


@bp.route('/schedule/<int:scheduling_id>', methods=['DELETE'])
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


@bp.route('/export-schedule', methods=['POST'])
def get_schedule_in_excel():
    email.send_email('test', 'besdaemon490@gmail.com', ['besvova490@gmail.com'], 'Test')
    resp = request.json['data']
    user = users_func.UserConf.get_user_object(resp['user_id'])
    user.launch_task('export_posts', 'Exporting posts...')
    db.session.commit()
    return jsonify({'msg': 'Schedule sanded to your email'}), 200
