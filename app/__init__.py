from config import Config
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @jwt.unauthorized_loader
    def my_unauthorized_callback(error_msg):
        return jsonify({'msg': 'User Unauthorized'}), 401

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.telebot import bp as telebot_bp
    app.register_blueprint(telebot_bp, url_prefix='/RDOALlvctMgPAwCCKDmMsb')

    return app


from app import models
