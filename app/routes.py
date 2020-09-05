from app import app, teacher_funcs
from flask import jsonify


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Home page', 'title': 'Home'}), 200


@app.route('/about', methods=['GET'])
def about():
    return jsonify({'message': 'About page', 'title': 'About'}), 200


@app.route('/blog', methods=['GET'])
def blog():
    return jsonify({'message': 'Blog page', 'title': 'Blog'}), 200


@app.route('/tutors', methods=['GET'])
def tutors_page():
    tutors = teacher_funcs.TeacherConf.teachers_list()
    resp = jsonify({'message': 'Tutors page', 'title': 'Tutors', 'data': tutors})
    return resp, 200


@app.route('/students', methods=['GET'])
def students_page():
    return jsonify({'message': 'Students page', 'title': 'Students'}), 200


@app.route('/subjects', methods=['GET'])
def subjects_page():
    return jsonify({'message': 'Subjects page', 'title': 'Subjects'}), 200
