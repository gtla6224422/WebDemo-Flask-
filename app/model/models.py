# app/models.py
# coding=utf-8

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

# 用户模型
class User(db.Model):
    __tablename__ = 'user_tbl'  # 显式指定表名为 user_tbl
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Integer, default=1)
    user_status = db.Column(db.Integer, default=1)
    create_time = db.Column(db.TIMESTAMP, server_default=func.now())  # 添加 create_time 字段，默认值为当前时间戳
    last_update_time = db.Column(db.TIMESTAMP, server_default=func.now())  # 添加 last_update_time 字段，默认值为当前时间戳
    
    def action_to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }