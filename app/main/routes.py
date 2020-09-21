from app import users_func, subject_func, scheduling_func, db
from app.main import main
from flask import jsonify, request
import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity


@main.route('/', methods=['GET'])
def index():
    resp = jsonify({'message': 'Home page', 'title': 'Home'})
    return resp, 200


@main.route('/about', methods=['GET'])
def about():
    return jsonify({'message': 'About page', 'title': 'About'}), 200


@main.route('/sign-up', methods=['POST'])
def user_create():
    user_data = request.json['data']
    create = users_func.UserConf.sign_up(user_data)
    return create


@main.route('/sign-in', methods=['POST'])
def user_sign_in():
    user_data = request.json['data']
    return users_func.UserConf.sign_in(user_data)


@main.route('/log-out', methods=['POST'])
def user_log_out():
    return users_func.UserConf.log_out()


@main.route('/tutors', methods=['GET'])
@jwt_required
def tutors_page():
    return users_func.UserConf.get_users_list(is_teacher=True)


@main.route('/students', methods=['GET'])
@jwt_required
def students_page():
    return users_func.UserConf.get_users_list(is_teacher=False)


@main.route('/subjects', methods=['GET'])
@jwt_required
def subjects():
    resp_subjects = subject_func.SubjectConf.get_subjects_list()
    return resp_subjects


@main.route('/profile', methods=['GET'])
@jwt_required
def user_profile():
    return users_func.UserConf.get_user_object(get_jwt_identity())


@main.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required
def student_page_update(user_id):
    data = request.json['data']
    resp = users_func.UserConf.update_user(user_id, data)
    return resp


@main.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required
def student_delete(user_id):
    resp = users_func.UserConf.user_delete(user_id)
    return resp


@main.route('/user/<int:user_id>/scheduling/<int:scheduling_id>', methods=['POST'])
@jwt_required
def scheduling_confirmation(user_id, scheduling_id):
    resp = scheduling_func.SchedulingConf.scheduling_confirmation(scheduling_id, user_id)
    return resp


@main.route('/user/<int:user_id>/schedule-not-confirmed', methods=['GET'])
@jwt_required
def schedule_confirmed(user_id):
    return users_func.UserConf.wait_for_confirmation(user_id), 200


@main.route('/user/<int:teacher_id>/<int:user_id>', methods=['POST'])
@jwt_required
def connect_user_teacher(teacher_id, user_id):
    resp = users_func.UserConf.connect_teacher_with_student(teacher_id, user_id)
    return resp


@main.route('/subjects', methods=['POST'])
@jwt_required
def subject_create():
    subject_data = request.json['data']
    create = subject_func.SubjectConf.create_subject(subject_data)
    return create


@main.route('/subjects/<int:subject_id>', methods=['PUT'])
@jwt_required
def subject_page_update(subject_id):
    data = request.json['data']
    resp = subject_func.SubjectConf.subject_update(subject_id, data)
    return resp


@main.route('/subjects/<int:subject_id>', methods=['DELETE'])
@jwt_required
def subject_delete(subject_id):
    resp = subject_func.SubjectConf.subject_delete(subject_id)
    return resp


@main.route('/subjects/<int:subject_id>', methods=['GET'])
@jwt_required
def subject_page(subject_id):
    resp = subject_func.SubjectConf.get_subject_by_id(subject_id)
    return resp


@main.route('/subjects/<int:subject_id>/<int:user_id>', methods=['POST'])
@jwt_required
def add_user_to_subject(user_id, subject_id):
    resp = users_func.UserConf.add_to_subject(user_id, subject_id)
    return resp


@main.route('/scheduling', methods=['POST'])
@jwt_required
def add_scheduling():
    data = request.json['data']
    data['time'] = datetime.datetime.strptime(data['time'], '%d-%m-%Y')
    resp = scheduling_func.SchedulingConf.add_scheduling(data['teacher'], data['student'], data['subject'], data['time'])
    return resp


@main.route('/scheduling/<int:scheduling_id>', methods=['DELETE'])
@jwt_required
def delete_scheduling(scheduling_id):
    resp = scheduling_func.SchedulingConf.delete_scheduling(scheduling_id)
    return resp


@main.route('/export-schedule', methods=['GET'])
@jwt_required
def get_schedule_in_excel():
    user = users_func.UserConf.get_user_object(get_jwt_identity())
    if user.get_task_in_progress('export_posts'):
        return jsonify({'msg': 'Task exist'}), 401
    user.launch_task('export_posts', 'Exporting posts...')
    db.session.commit()
    return jsonify({'msg': 'Schedule sanded to your email'}), 200

