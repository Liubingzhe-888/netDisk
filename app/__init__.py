from logging import log
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_migrate import Migrate
#from flask_cors import *

db = SQLAlchemy()
migrate = Migrate()


# 创建工厂函数，：将app所有配置，配置到app上，然后初始化app
def create_app(config_name):
    # config_name是应用app的配置名，参数
    app = Flask(__name__)
    # CORS(app, resources=r'/*')
    # 使用from_object方法，将配置参数配置到应用对象上去
    app.config.from_object(config[config_name])
    #CORS(app, supports_credentials=True) 
    config[config_name].init__app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    # 将创建的蓝本绑定注册到应用实例app上
    from app.web import web
    from app.api_2_0 import API2
    from app.logic import logic
    app.register_blueprint(web,url_prefix='/')
    app.register_blueprint(API2,url_prefix='/api')
    return app
