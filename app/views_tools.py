from flask import Blueprint, request, jsonify,json,Response
#from .model.models import Order # 导入 models 模块
import os
from jsonpath_ng import parse
import logging
import json as simplejson


# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Tools_bp = Blueprint('tools_bp', __name__)
#公共方法，考虑提取
def find_field_paths(data, field_name, current_path="$"):
    paths = []

    def _find_paths(obj, path):
        if isinstance(obj, dict):
            for key, value in obj.items():
                # 如果字段名包含特殊字符，使用引号将其括起来
                quoted_key = f"'{key}'" if any(c in key for c in " -./") else key
                new_path = f"{path}.{quoted_key}" if path != "$" else f"$.{quoted_key}"
                
                if key == field_name:
                    paths.append(new_path)
                
                _find_paths(value, new_path)
        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                new_path = f"{path}[{index}]"
                _find_paths(item, new_path)


    _find_paths(data, current_path)
    return paths

def test_jsonpath_expression(data, path):
    try:
        jsonpath_expr = parse(path)
        matches = [match.value for match in jsonpath_expr.find(data)]
        return matches
    except Exception as e:
        logger.error(f"无效的 JSONPath 表达式: {path}, 错误信息: {str(e)}")
        return None

@Tools_bp.route('/Sum_json', methods=['POST'])
def Sum_json():
    # 获取请求中的 JSON 数据
    if not request.is_json:
        logger.error("请求不是 JSON 格式")
        return jsonify(
            status_code=10002,
            error="请求必须是 JSON 格式"
        ), 400

    data = request.get_json()
    logger.debug(f"接收到的 JSON 数据: {data}")

    if not data or 'field_name' not in data:
        logger.error("缺少必要字段")
        return jsonify(
            status_code=10003,
            error="缺少必要字段"
        ), 400

    field_name = data.get('field_name')

    # 获取当前应用的根目录
    app_root = os.path.dirname(os.path.abspath(__file__))
    coco_file_path = os.path.join(app_root, 'coco.txt')

    # 检查文件是否存在
    if not os.path.exists(coco_file_path):
        logger.error(f"coco.txt 文件未找到: {coco_file_path}")
        return jsonify(
            status_code=10004,
            error="coco.txt 文件未找到"
        ), 404

    try:
        # 读取 coco.txt 文件内容，指定编码为 UTF-8 并处理 BOM
        with open(coco_file_path, 'r', encoding='utf-8-sig') as file:
            coco_data = json.load(file)
            logger.debug(f"成功读取 coco.txt 文件: {coco_data}")
    except FileNotFoundError:
        logger.error(f"coco.txt 文件未找到: {coco_file_path}")
        return jsonify(
            status_code=10004,
            error="coco.txt 文件未找到"
        ), 404
    except json.JSONDecodeError as e:
        logger.error(f"coco.txt 文件内容不是有效的 JSON 格式: {str(e)}")
        return jsonify(
            status_code=10005,
            error="coco.txt 文件内容不是有效的 JSON 格式"
        ), 400
    except UnicodeDecodeError as e:
        logger.error(f"无法解码文件: {str(e)}")
        return jsonify(
            status_code=10005,
            error="无法解码文件"
        ), 400

    # 找到所有包含指定字段名的路径
    field_paths = find_field_paths(coco_data, field_name)

    if not field_paths:
        logger.error(f"没有找到字段 '{field_name}'")
        return jsonify(
            status_code=10007,
            error=f"没有找到字段 '{field_name}'"
        ), 404

    # 提取匹配的字段
    matches = []
    numeric_matches = []  # 用于存储数值类型的匹配项
    for path in field_paths:
        extracted_data = test_jsonpath_expression(coco_data, path)
        if extracted_data:
            matches.extend(extracted_data)
            for value in extracted_data:
                if isinstance(value, (int, float)):
                    numeric_matches.append(value)
        else:
            logger.error(f"无效的 JSONPath 表达式: {path}, 无法提取数据")

    if not matches:
        logger.error(f"没有找到可提取的字段 '{field_name}'")
        return jsonify(
            status_code=10008,
            error=f"没有找到可提取的字段 '{field_name}'"
        ), 404

    # 计算合计值（仅当有数值类型字段时）
    total = None
    if numeric_matches:
        total = round(sum(numeric_matches), 4)  # 保留小数点后四位

    # 返回结果
    response_data = {
        "status_code": 200,
        "message": "成功提取并计算",
        "data": {
            "fields": matches
        }
    }

    # 只有当有数值类型字段时才输出 total 字段
    if total is not None:
        response_data["data"]["total"] = total

    return jsonify(response_data), 200


@Tools_bp.route('/Get_field', methods=['POST'])
def get_field():
    """获取指定字段的所有值，并根据参数决定是否去重"""
    # 获取请求中的 JSON 数据
    if not request.is_json:
        logger.error("请求不是 JSON 格式")
        return jsonify(
            status_code=10002,
            error="请求必须是 JSON 格式"
        ), 400

    data = request.get_json()
    logger.debug(f"接收到的 JSON 数据: {data}")

    # 检查必要字段
    if not data or 'field_name' not in data:
        logger.error("缺少必要字段")
        return jsonify(
            status_code=10003,
            error="缺少必要字段"
        ), 400

    field_name = data.get('field_name')
    distinct = data.get('distinct', 1)  # 默认启用去重

    # 获取当前应用的根目录
    app_root = os.path.dirname(os.path.abspath(__file__))
    coco_file_path = os.path.join(app_root, 'coco.txt')

    # 检查文件是否存在
    if not os.path.exists(coco_file_path):
        logger.error(f"coco.txt 文件未找到: {coco_file_path}")
        return jsonify(
            status_code=10004,
            error="coco.txt 文件未找到"
        ), 404

    try:
        # 读取 coco.txt 文件内容，指定编码为 UTF-8 并处理 BOM
        with open(coco_file_path, 'r', encoding='utf-8-sig') as file:
            coco_data = json.load(file)
            logger.debug(f"成功读取 coco.txt 文件: {coco_data}")
    except FileNotFoundError:
        logger.error(f"coco.txt 文件未找到: {coco_file_path}")
        return jsonify(
            status_code=10004,
            error="coco.txt 文件未找到"
        ), 404
    except json.JSONDecodeError as e:
        logger.error(f"coco.txt 文件内容不是有效的 JSON 格式: {str(e)}")
        return jsonify(
            status_code=10005,
            error="coco.txt 文件内容不是有效的 JSON 格式"
        ), 400
    except UnicodeDecodeError as e:
        logger.error(f"无法解码文件: {str(e)}")
        return jsonify(
            status_code=10005,
            error="无法解码文件"
        ), 400

    # 找到所有包含指定字段名的路径
    field_paths = find_field_paths(coco_data, field_name)

    if not field_paths:
        logger.error(f"没有找到字段 '{field_name}'")
        return jsonify(
            status_code=10007,
            error=f"没有找到字段 '{field_name}'"
        ), 404

    # 提取匹配的字段值
    matches = []
    for path in field_paths:
        extracted_data = test_jsonpath_expression(coco_data, path)
        if extracted_data:
            matches.extend(extracted_data)
        else:
            logger.error(f"无效的 JSONPath 表达式: {path}, 无法提取数据")

    if not matches:
        logger.error(f"没有找到可提取的字段 '{field_name}'")
        return jsonify(
            status_code=10008,
            error=f"没有找到可提取的字段 '{field_name}'"
        ), 404

    # 根据 distinct 参数决定是否去重
    if distinct == 1:
        # 对字段值去重，并保持原始顺序
        unique_matches = []
        seen = set()
        for value in matches:
            if value not in seen:
                unique_matches.append(value)
                seen.add(value)
        matches = unique_matches

    # 返回结果
    response_data = {
        "status_code": 200,
        "message": "成功提取字段",
        "data": {
            "fields": matches
        }
    }

    return jsonify(response_data), 200


