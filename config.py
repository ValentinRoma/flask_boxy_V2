import os
basedir = os.path.abspath(os.path.dirname(__file__))
DB_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{database_name}".format(
    username = 'Valentin10romani',
    password = "",
    hostname = 'Valentin10romaniello.mysql.pythonanywhere-services.com',
    database_name = 'Valentin10romani$produV1'
)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    #FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    #FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    
    @staticmethod
    def init_app(app):
        pass
    
    
class DevelopmentConfig(Config):
    DEBUG = True
    #MAIL_SERVER = 'smtp.googlemail.com'
    #MAIL_PORT = 587
    #MAIL_USE_TLS = True
    #MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    #MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'login.db')
    SECRET_KEY = 'cambia-esta-clave-secreta'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #app.config['SECRET_KEY'] = 'cambia-esta-clave-secreta'
    
class TestingConfig(Config):
     TESTING = True
     SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
 'sqlite:///' + os.path.join(basedir, 'login.db')
 

# class ProductionConfig(Config):
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#  'sqlite:///' + os.path.join(basedir, 'datas.db')

class ProductionConfig:
    SECRET_KEY = "dsg<dmsgm<ed+fmf,"
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
 
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default':DevelopmentConfig
}