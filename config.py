class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'yYrdj_1iAuCJBZo1lzK26Q'
    MAIL_SERVER = "smtp.zoho.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'support@flippinapp.com'
    MAIL_PASSWORD = 'aquaQUEEF8008'


class LocalConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:aquaQUEEF8008@localhost:3306/flippin_flask'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False