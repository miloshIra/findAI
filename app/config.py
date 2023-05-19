import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_USL') or 'postgresql://postgres:postgres@localhost/findAIdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    os.environ['FLASK_DEBUG'] = 'True'

    #flask-mail
    MAIL_DEFAULT_SENDER = 'dontreply@ariton.ai'
    MAIL_SERVER='sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = '1d5427cc11d476'
    MAIL_PASSWORD= '95653137ad9ea6'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    