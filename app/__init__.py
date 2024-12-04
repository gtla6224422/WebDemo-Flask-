# app/__init__.py

from flask import Flask
from .conf.config import Config
from .model.models import db
from .views_login import login_bp,bcrypt # 导入蓝图
from .views_order import Order_bp # 导入蓝图
from .views_tools import Tools_bp
from flask_migrate import migrate
import redis

app = None

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
    
    # 初始化 Redis
    app.redis = redis.StrictRedis(host='1.14.155.39', port=6379, db=0,password='lo633533')

    # 注册蓝图
    with app.app_context():
        from .views_UserInfo import UserInfo_bp
        app.register_blueprint(UserInfo_bp,__name__ = 'UserInfo_bp')

    app.register_blueprint(login_bp,__name__ = 'login_bp')
    app.register_blueprint(Order_bp,__name__ = 'Order_bp')
    app.register_blueprint(Tools_bp,__name__ = 'tools_bp')
    
    return app