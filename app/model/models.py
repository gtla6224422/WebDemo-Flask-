# app/models.py
# coding=utf-8

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import random
from datetime import datetime,timezone

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
    del_flag = db.Column(db.Integer, default=0)

    def action_to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "del_flag": self.del_flag
        }
    
# 订单详情模型
class Order(db.Model):
    __tablename__ = 'order_tbl'  # 显式指定表名为 order_details
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer)
    custom_id = db.Column(db.String(255))
    order_cost = db.Column(db.DECIMAL(10, 2))
    insurance_cost = db.Column(db.DECIMAL(10, 2))
    insurance_type = db.Column(db.Integer)
    create_time = db.Column(db.TIMESTAMP, server_default=func.now())  # 添加 create_time 字段，默认值为当前时间戳
    last_update_time = db.Column(db.TIMESTAMP, server_default=func.now())  # 添加 last_update_time 字段，默认值为当前时间戳
    remark1 = db.Column(db.String(255))
    remark2 = db.Column(db.String(255))
    remark3 = db.Column(db.String(255))
    del_flag = db.Column(db.Integer,default=0)

    def generate_order_id(self):
        # 生成一个8位的order_id，前4位为1000，后4位为随机数
        random_part = random.randint(0, 9999)
        order_id = f"1000{random_part:04d}"
        return order_id


    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "custom_id": self.custom_id,
            "order_cost": str(self.order_cost),
            "insurance_cost": str(self.insurance_cost),
            "insurance_type": self.insurance_type,
            "remark1": self.remark1,
            "remark2": self.remark2,
            "remark3": self.remark3,
            "del_flag": self.del_flag
        }