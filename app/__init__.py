import rq
import logging
import os
from config import Config
from logging.handlers import SMTPHandler, RotatingFileHandler
from redis import Redis
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from openpyxl import Workbook

jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
wb = Workbook()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('beetroot_project-tasks', connection=app.redis)
    CORS(app, supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)

    mail.init_app(app)

    @jwt.unauthorized_loader
    def my_unauthorized_callback(error_msg):
        return jsonify({'msg': 'User Unauthorized'}), 401

    jwt.init_app(app)
    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    from app.telebot import bp as telebot_bp
    app.register_blueprint(telebot_bp, url_prefix='/RDOALlvctMgPAwCCKDmMsb')

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['MAIL_USERNAME'],
                subject='Beetroot project Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/beetroot-project.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Beetroot besvova490 startup')

    return app


from app import models
