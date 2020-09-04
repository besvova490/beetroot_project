from app import app
from flask import jsonify


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Home page', 'title': 'Home'}), 200


@app.route('/about', methods=['GET'])
def about():
    return jsonify({'message': 'About page', 'title': 'About'}), 200


@app.route('/tutors', methods=['GET'])
def tutors_page():
    return jsonify({'message': 'Tutors page', 'title': 'Tutors'}), 200


@app.route('/students', methods=['GET'])
def students_page():
    return jsonify({'message': 'Students page', 'title': 'Students'}), 200


@app.route('/subjects', methods=['GET'])
def subjects_page():
    return jsonify({'message': 'Subjects page', 'title': 'Subjects'}), 200
