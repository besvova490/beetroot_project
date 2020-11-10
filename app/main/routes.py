from app import db, models
from app.main import main
from app.models_conf_classes import UserConf, SubjectConf, SchedulingConf
from flask import jsonify, request
import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity


@main.route('/', methods=['GET'])
def index():
    resp = jsonify({'message': 'Home page', 'title': 'Home'})
    return resp, 200


@main.route('/about/', methods=['GET'])
def about():
    return jsonify({'message': 'About page', 'title': 'About'}), 200


@main.route('/sign-up', methods=['POST'])
def user_create():
    user_data = request.json['data']
    create = UserConf.sign_up(user_data)
    return create


@main.route('/sign-in', methods=['POST'])
def user_sign_in():
    user_data = request.json['data']
    return UserConf.sign_in(user_data)


@main.route('/log-out', methods=['POST'])
def user_log_out():
    return UserConf.log_out()


@main.route('/users', methods=['GET'])
def users_page():
    return UserConf.get_objects_dict_list_or_404(models.User, **request.args)


@main.route('/subjects', methods=['GET'])
@jwt_required
def subjects():
    return SubjectConf.get_objects_dict_list_or_404(models.Subject, **request.args)


@main.route('/profile', methods=['GET'])
@jwt_required
def user_profile():
    user_id = get_jwt_identity()
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
    return UserConf.get_obj_dict_or_404(models.User, user_id)


@main.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required
def user_page_update(user_id):
    data = request.json['data']
    resp = UserConf.update_obj(models.User, user_id, db, data)
    return resp


@main.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required
def user_delete(user_id):
    user = UserConf.get_obj(models.User, user_id)
    return UserConf.delete_object(user, db)


@main.route('/subjects', methods=['POST'])
@jwt_required
def subject_create():
    subject_data = request.json['data']
    create = SubjectConf.create_subject(subject_data)
    return create


@main.route('/subjects/<int:subject_id>', methods=['PUT'])
@jwt_required
def subject_page_update(subject_id):
    data = request.json['data']
    resp = SubjectConf.update_obj(models.Subject, subject_id, db, data)
    return resp


@main.route('/subjects/<int:subject_id>', methods=['DELETE'])
@jwt_required
def subject_delete(subject_id):
    subject = SubjectConf.get_obj(models.Subject, subject_id)
    resp = SubjectConf.delete_object(subject, db)
    return resp


@main.route('/subjects/<int:subject_id>', methods=['GET'])
@jwt_required
def subject_page(subject_id):
    return SubjectConf.get_obj_dict_or_404(models.Subject, subject_id)


@main.route('/scheduling', methods=['POST'])
@jwt_required
def add_scheduling():
    data = request.json['data']
    data['lesson_time'] = datetime.datetime.strptime(data['lesson_time'], '%Y-%m-%dT%H:%M:%SZ')
    resp = SchedulingConf.add_scheduling(data['subject'], data['lesson_time'], data['users'])
    return resp


@main.route('/schedule/<int:scheduling_id>', methods=['GET'])
def scheduling_confirmation(scheduling_id):
    query = request.args
    if query:
        if query['set_conformation'] == 'Flase':
            return SchedulingConf.delete_scheduling(scheduling_id)
        return SchedulingConf.scheduling_confirmation(scheduling_id, user_id=query['user_id'])
    return SchedulingConf.get_obj_dict_or_404(models.Scheduling, scheduling_id)


@main.route('/scheduling/<int:scheduling_id>', methods=['DELETE'])
@jwt_required
def delete_scheduling(scheduling_id):
    resp = SchedulingConf.delete_scheduling(scheduling_id)
    return resp


@main.route('/export-schedule', methods=['GET'])
@jwt_required
def get_schedule_in_excel():
    user = UserConf.get_obj(models.User, get_jwt_identity())
    if user.get_task_in_progress('export_posts'):
        return jsonify({'msg': 'Task exist'}), 401
    user.launch_task('export_posts', 'Exporting posts...')
    db.session.commit()
    return jsonify({'msg': 'Schedule sanded to your email'}), 200
