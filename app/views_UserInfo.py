# app/views_action.py
# coding=utf-8

from flask import Blueprint, request, jsonify,json,current_app
from .model.models import User # 导入 models 模块
from . import create_app
UserInfo_bp = Blueprint('UserInfo_bp', __name__)
import logging

#grafana-prometheus
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@UserInfo_bp.route('/get_user', methods=['GET'])
def get_user():
    # 获取查询参数
    id = request.args.get('id', type=int)
    role = request.args.get('role', type=int)
    
    if id is None or role is None:
        return jsonify({
            "status_code": 10001,
            "error": "Missing required parameters"
            }), 400
    
    # 模拟数据查询，入参传什么就返回什么
    user_data = {
        "id": id,
        "role": role,
        "username": f"user_{id}",
        "role_name": f"role_{role}"
    }
    
    return jsonify(user_data), 200

@UserInfo_bp.route('/UserInfo', methods=['POST'])
def GetUserInfo():
     # 获取 JSON 数据
    if not request.is_json:
        return jsonify({
            "status_code": 10002,
            "error": "请求必须是 JSON 格式"
            }), 400
    
    data = request.get_json()
    
    if not data or 'role' not in data:
        return jsonify({
            "status_code": 10003,
            "error": "缺少必要字段"
            }), 400
    try:
        #userid = int(data.get('userid'))
        #username = data.get('username')
        #id = int(data.get('id'))
        role = int(data.get('role'))
    except (ValueError, TypeError):
        return jsonify({
            "status_code": 10004,
            "error": "无效的数据类型"
            }), 400
    
    # 生成缓存键
    cache_key = f'users_with_role:{role}'
   
     # 从 Redis 中获取数据
    cached_data = current_app.redis.get(cache_key)
    if cached_data:
        return jsonify(json.loads(cached_data.decode('utf-8'))), 200
    
     # 查询数据库
    users = User.query.filter_by(role=role).all()
    
    if users:
        # 将每个用户对象转换为字典
        user_dicts = [User.action_to_dict() for User in users]

        # 将数据存储到 Redis 中
        current_app.redis.set(cache_key, jsonify(user_dicts).data, ex=600)  # 缓存10分钟

        return jsonify(user_dicts), 200
    else:
        return jsonify({
            "status_code": 10005,
            "error": "未找到具有指定角色的用户"
            }), 404
    
    return jsonify(user_data), 201