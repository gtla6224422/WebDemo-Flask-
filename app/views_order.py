from flask import Blueprint, request, jsonify,json,current_app
from .model.models import Order # 导入 models 模块

from . import db

Order_bp = Blueprint('order_bp', __name__)
@Order_bp.route('/Create_order', methods=['POST'])
def Create_order():
    # 获取 JSON 数据
    if not request.is_json:
        return jsonify({
            "status_code": 10002,
            "error": "请求必须是 JSON 格式"
        }), 400

    data = request.get_json()

    if not data or 'custom_id' not in data or 'order_cost' not in data:
        return jsonify({
            "status_code": 10003,
            "error": "缺少必要字段"
        }), 400

    try:
        # 对入参json进行提取转换成入库字段
        
        custom_id = int(data.get('custom_id'))
        order_cost = round(float(data.get('order_cost')), 2)
        insurance_cost = round(float(data.get('insurance_cost')), 2)
        insurance_type = int(data.get('insurance_type'))
    except (ValueError, TypeError):
        return jsonify({
            "status_code": 10004,
            "error": "无效的数据类型"
        }), 400

    # 生成唯一的订单ID
    order_id = Order().generate_order_id()

    # 检查订单ID是否已存在
    existing_order = Order.query.filter_by(order_id=order_id).first()
    if existing_order:
        return jsonify({
            "status_code": 10006,
            "error": "生成的订单号已存在"
        }), 400

    # 创建新的订单记录
    new_order = Order(
        order_id=order_id,
        custom_id=custom_id,
        order_cost=order_cost,
        insurance_cost=insurance_cost,
        insurance_type=insurance_type
    )

    # 将新订单记录添加到数据库
    try:
        db.session.add(new_order)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status_code": 10005,
            "error": f"数据库操作失败: {str(e)}"
        }), 500

    # 返回成功响应
    return jsonify({
        "status_code": 200,
        "message": "订单创建成功",
        "data": new_order.to_dict()
    }), 201