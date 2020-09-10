from app import app, users_func, subject_func, scheduling_func
from flask import jsonify, request
import datetime


@app.route('/', methods=['GET'])
def index():
    resp = jsonify({'message': 'Home page', 'title': 'Home'})
    return resp, 200


@app.route('/about', methods=['GET'])
def about():
    return jsonify({'message': 'About page', 'title': 'About'}), 200


@app.route('/blog', methods=['GET'])
def blog():
    return jsonify({'message': 'Blog page', 'title': 'Blog'}), 200


@app.route('/sign-up', methods=['POST'])
def user_create():
    user_data = request.json['data']
    create = users_func.UserConf.sign_up(user_data)
    return create


@app.route('/sign-in', methods=['POST'])
def user_sign_in():
    user_data = request.json['data']
    return users_func.UserConf.sign_in(user_data)


@app.route('/log-out', methods=['POST'])
def user_log_out():
    return users_func.UserConf.log_out()


@app.route('/tutors', methods=['GET'])
def tutors_page():
    tutors = users_func.UserConf.get_users_list(is_teacher=True)
    resp = jsonify({'message': 'Tutors page', 'title': 'Tutors', 'data': tutors})
    return resp, 200


@app.route('/students', methods=['GET'])
def students_page():
    students = users_func.UserConf.get_users_list(is_teacher=False)
    resp = jsonify({'message': 'Students page', 'title': 'Students', 'data': students})
    return resp, 200


@app.route('/subjects', methods=['GET'])
def subjects():
    subjects = subject_func.SubjectConf.get_subjects_list()
    resp = jsonify({'message': 'Subjects page', 'title': 'Subjects', 'data': subjects})
    return resp, 200


@app.route('/user/<int:user_id>', methods=['GET'])
def user_page(user_id):
    user = users_func.UserConf.get_user_object(user_id)
    resp = users_func.UserConf.get_user_info(user)
    return jsonify({'massage': 'User page', 'data': resp}), 200


@app.route('/user/<int:user_id>', methods=['PUT'])
def student_page_update(user_id):
    data = request.json['data']
    resp = users_func.UserConf.update_user(user_id, data)
    return resp


@app.route('/user/<int:user_id>', methods=['DELETE'])
def student_delete(user_id):
    resp = users_func.UserConf.user_delete(user_id)
    return resp


@app.route('/subjects', methods=['POST'])
def subject_create():
    subject_data = request.json['data']
    create = subject_func.SubjectConf.create_subject(subject_data)
    return create


@app.route('/subjects/<int:subject_id>', methods=['PUT'])
def subject_page_update(subject_id):
    data = request.json['data']
    resp = subject_func.SubjectConf.subject_update(subject_id, data)
    return resp


@app.route('/subjects/<int:subject_id>', methods=['DELETE'])
def subject_delete(subject_id):
    resp = subject_func.SubjectConf.subject_delete(subject_id)
    return resp


@app.route('/subjects/<int:subject_id>', methods=['GET'])
def subject_page(subject_id):
    resp = subject_func.SubjectConf.get_subject_by_id(subject_id)
    return resp


@app.route('/subjects/<int:subject_id>/<int:user_id>', methods=['POST'])
def add_user_to_subject(user_id, subject_id):
    resp = users_func.UserConf.add_to_subject(user_id, subject_id)
    return resp


@app.route('/scheduling', methods=['POST'])
def add_scheduling():
    data = request.json['data']
    data['time'] = datetime.datetime.strptime(data['time'], '%d-%m-%Y')
    resp = scheduling_func.SchedulingConf.add_scheduling(data['teacher'], data['student'], data['subject'], data['time'])
    return resp


@app.route('/user/<int:user_id>/scheduling/<int:scheduling_id>', methods=['POST'])
def scheduling_confirmation(user_id, scheduling_id):
    teacher = users_func.UserConf.get_user_object(user_id).full_name
    resp = scheduling_func.SchedulingConf.scheduling_confirmation(scheduling_id)
    students = resp[0].json['student']
    for student in students:
        message = f'Teacher: {teacher} approved lesson: ' \
                  f'{resp[0].json["subject"]} \nLesson time: {resp[0].json["time"]}'
        users_func.UserConf.send_message(int(student), message)
    return resp


@app.route('/user/<int:user_id>/schedule/not-confirmed', methods=['GET'])
def schedule_confirmed(user_id):
    return users_func.UserConf.wait_for_confirmation(user_id), 200


@app.route('/telegram-check', methods=['POST'])
def telegram_check():
    resp = users_func.UserConf.check_telegram(request.json['data'])
    return resp


@app.route('/telegram-sign-up', methods=['POST'])
def user_create_telegram():
    user_data = request.json['data']
    create = users_func.UserConf.sign_up_telegram(user_data)
    return create


@app.route('/telegram-sign-in', methods=['POST'])
def user_sign_in_telegram():
    user_data = request.json['data']
    return users_func.UserConf.sign_in_telegram(user_data)


@app.route('/telegram-user/<int:teacher_id>/<int:user_id>', methods=['POST'])
def connect_user_teacher(teacher_id, user_id):
    resp = users_func.UserConf.connect_teacher_with_student(teacher_id, user_id)
    return resp
