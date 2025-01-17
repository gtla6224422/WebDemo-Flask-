from flask import Blueprint, request, jsonify,json,Response,current_app
#from .model.models import Order # 导入 models 模块
Log_bp = Blueprint('log_bp', __name__)
from jsonpath_ng import parse
import logging
from prometheus_client import generate_latest, Counter, Gauge, Histogram
from prometheus_flask_exporter import PrometheusMetrics
from .conf.config import Config

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义prometheus指标
REQUEST_COUNT = Counter('request_count', 'App Request Count')
REQUEST_LATENCY = Histogram('request_latency', 'Request latency')
IN_PROGRESS = Gauge('in_progress', 'Number of requests in progress')

@Log_bp.route('/metrics')
def metrics_endpoint():
    #return metrics.get_metrics()
    return Response(generate_latest(), mimetype='text/plain')
