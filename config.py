class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'yYrdj_1iAuCJBZo1lzK26Q'


class LocalConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:aquaQUEEF8008@localhost:3306/flippin_flask'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False