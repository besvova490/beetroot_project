from app import app, users_func, subject_func
from flask import jsonify, request


@app.route('/', methods=['GET'])
def index():
    resp = jsonify({'message': 'Home page', 'title': 'Home'})
    resp.set_cookie('hello', 'test', samesite='None', secure=True)
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
    create = users_func.UserConf.sign_up(**user_data)
    return create


@app.route('/sign-in', methods=['POST'])
def user_sign_in():
    print(1222222, request.json)
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


@app.route('/tutors/<int:tutors_id>', methods=['GET'])
def tutor_page(tutors_id):
    resp = users_func.UserConf.get_user_dy_id(tutors_id)
    return resp


@app.route('/tutors/<int:tutors_id>', methods=['PUT'])
def tutor_page_update(tutors_id):
    data = request.json['data']
    resp = users_func.UserConf.update_user(tutors_id, data)
    return resp


@app.route('/tutors/<int:tutors_id>', methods=['DELETE'])
def tutor_delete(tutors_id):
    resp = users_func.UserConf.user_delete(tutors_id)
    return resp


@app.route('/students', methods=['GET'])
def students_page():
    students = users_func.UserConf.get_users_list(is_teacher=False)
    resp = jsonify({'message': 'Students page', 'title': 'Students', 'data': students})
    return resp, 200


@app.route('/students/<int:students_id>', methods=['GET'])
def student_page(students_id):
    resp = users_func.UserConf.get_user_dy_id(students_id)
    return resp


@app.route('/students/<int:students_id>', methods=['PUT'])
def student_page_update(students_id):
    data = request.json['data']
    resp = users_func.UserConf.update_user(students_id, data)
    return resp


@app.route('/students/<int:students_id>', methods=['DELETE'])
def student_delete(students_id):
    resp = users_func.UserConf.user_delete(students_id)
    return resp


@app.route('/subjects', methods=['GET'])
def subjects_page():
    subjects = subject_func.SubjectConf.get_subjects_list()
    resp = jsonify({'message': 'Subjects page', 'title': 'Subjects', 'data': subjects})
    return resp, 200


@app.route('/subjects/<int:subject_id>', methods=['GET'])
def subject_page(subject_id):
    resp = subject_func.SubjectConf.get_subject_by_id(subject_id)
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

