from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get('DEVELOPMENT_DATABASE_URI')
    SECRET_KEY = environ.get('DEVELOPMENT_SECRET_KEY')


class TestConfig:
    TESTING = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get('PRODUCTION_DATABASE_URI')
    SECRET_KEY = environ.get('PRODUCTION_SECRET_KEY')

