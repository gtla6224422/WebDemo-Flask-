# app/__init__.py

from flask import Flask
from .conf.config import Config
from .model.models import db
from .views_login import login_bp,bcrypt # 导入蓝图
from .views_action import action_bp # 导入蓝图
from flask_migrate import migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化 Bcrypt
    bcrypt.init_app(app)
    
    # 初始化 Flask-Migrate
    #migrate.init_app(app, db)
    migrate.__init__(app, db)
    
    # 注册蓝图
    app.register_blueprint(login_bp,__name__ = 'login_bp')
    app.register_blueprint(action_bp,__name__ = 'action_bp')
    
    return app