import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    APP_SETTINGS = os.environ.get('APP_SETTINGS') or 'config.Config"'
    DEBUG = os.environ.get('FLASK_DEBUG') or 0
    TESTING = os.environ.get('FLASK_TESTING') or 0
    CSRF_ENABLED = os.environ.get('CSRF_ENABLED') or 1
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    APP_SECRET = os.environ.get('APP_SECRET') or 'SAJHF)HAw98heoahsokehI)ASHDF*Hgmsu9dhg'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or 0
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret'
    JWT_TOKEN_LOCATION = os.environ.get('JWT_TOKEN_LOCATION') or ['cookies']
    JWT_COOKIE_CSRF_PROTECT = os.environ.get('JWT_COOKIE_CSRF_PROTECT') or 0
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 465
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or ''
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or 0
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') or 1
    JWT_COOKIE_SECURE = os.environ.get('JWT_COOKIE_SECURE') or 0
    JWT_COOKIE_SAMESITE = os.environ.get('JWT_COOKIE_SAMESITE') or 'None'
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
