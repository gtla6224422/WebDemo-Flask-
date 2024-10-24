# app/routes.py

from flask import Blueprint, request, jsonify
from .model.models import User # 导入 models 模块

action_bp = Blueprint('action_bp', __name__)

@action_bp.route('/get_user', methods=['GET'])
def get_user():
    # 获取查询参数
    id = request.args.get('id', type=int)
    role = request.args.get('role', type=int)
    
    if id is None or role is None:
        return jsonify({"error": "Missing required parameters"}), 400
    
    # 模拟数据查询
    user_data = {
        "id": id,
        "role": role,
        "username": f"user_{id}",
        "role_name": f"role_{role}"
    }
    
    return jsonify(user_data), 200

@action_bp.route('/action', methods=['POST'])
def action():
     # 获取 JSON 数据
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    
    if not data or 'role' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    try:
        #userid = int(data.get('userid'))
        #username = data.get('username')
        #id = int(data.get('id'))
        role = int(data.get('role'))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data types"}), 400
    
     # 查询数据库
    users = User.query.filter_by(role=role).all()
    
    if users:
        # 将每个用户对象转换为字典
        user_dicts = [User.action_to_dict() for User in users]
        return jsonify(user_dicts), 200
    else:
        return jsonify({"error": "No users found with the specified role"}), 404
    
    return jsonify(user_data), 201