import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_USL') or 'postgresql://postgres:postgres@localhost/findAIdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    os.environ['FLASK_DEBUG'] = 'True'
