import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__name__))
# 创建应用app的基础配置类
class config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is hard secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    API_DOC_MEMBER = ['api', 'platform']
    @staticmethod
    def init__app(app):
        pass
class DevelopmentConfig(config):
    # 设置数据库uri，拼接路径
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
class ProductionConfig(config):
    pass
# 做成一个字典，供后面选择。
config = {
    'default': DevelopmentConfig
}
