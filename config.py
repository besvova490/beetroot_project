import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    APP_SECRET = 'SAJHF)HAw98heoahsokehI)ASHDF*Hgmsu9dhg'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret'
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'besdaemon490@gmail.com'
    MAIL_PASSWORD = '55nibipi'
    MAIL_USE_TLS = True
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'None'
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
