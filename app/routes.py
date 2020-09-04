from app import app
from flask import jsonify


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Home page', 'title': 'Home'}), 200


@app.route('/about', methods=['GET'])
def about():
    return jsonify({'message': 'About page', 'title': 'About'}), 200
