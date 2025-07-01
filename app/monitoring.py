import time
import sys
import io
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
from flask import request, g, Response

# 尝试设置 UTF-8 编码（可选）
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except:
    pass

class PrometheusMonitor:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PrometheusMonitor, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, app=None):
        if self._initialized:
            return
        self._initialized = True
        
        # 定义 Prometheus 指标
        self.REQUEST_COUNT = Counter(
            'flask_http_request_count',
            '接口请求总数',
            ['method', 'endpoint', 'http_status', 'blueprint']
        )
        
        self.REQUEST_LATENCY = Histogram(
            'flask_http_request_latency_seconds',
            '接口请求延迟',
            ['method', 'endpoint', 'blueprint'],
            buckets=[0.01, 0.05, 0.1, 0.5, 1, 2, 5]
        )
        
        self.REQUEST_SIZE = Histogram(
            'flask_http_request_size_bytes',
            '请求体大小',
            ['method', 'endpoint', 'blueprint'],
            buckets=[100, 500, 1000, 5000, 10000, 50000, 100000]
        )
        
        self.RESPONSE_SIZE = Histogram(
            'flask_http_response_size_bytes',
            '响应体大小',
            ['method', 'endpoint', 'blueprint', 'http_status'],
            buckets=[100, 500, 1000, 5000, 10000, 50000, 100000]
        )
        
        # 添加调试标志
        self.debug = True
        
        # 如果提供了app，立即初始化
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """初始化应用并注册中间件"""
        self.app = app
        
        # 注册全局钩子
        app.before_request(self._before_request)
        app.after_request(self._after_request)
        
        # 直接添加/metrics路由，不使用装饰器
        app.add_url_rule(
            '/metrics', 
            'prometheus_metrics', 
            self.metrics_view,
            methods=['GET']
        )
        
        if self.debug:
            print("Prometheus监控已初始化")  # 移除特殊字符
    
    def _before_request(self):
        """内部 before_request 实现"""
        # 跳过/metrics端点自身
        if request.path == '/metrics':
            return
        
        # 记录开始时间
        g.start_time = time.time()
        
        # 记录请求体大小
        if request.content_length:
            g.request_size = request.content_length
        else:
            # 获取请求数据长度（谨慎使用，可能影响性能）
            g.request_size = len(request.get_data()) if request.get_data() else 0
        
        # 调试日志
        if self.debug:
            print(f"开始请求: {request.method} {request.path}")  # 移除特殊字符
    
    def _after_request(self, response):
        """内部 after_request 实现"""
        # 跳过/metrics端点自身
        if request.path == '/metrics':
            return response
        
        # 检查是否有开始时间
        if not hasattr(g, 'start_time'):
            if self.debug:
                print(f"警告: before_request 未设置 g.start_time for {request.path}")  # 移除特殊字符
            return response
        
        try:
            # 获取请求信息
            latency = time.time() - g.start_time
            endpoint = request.endpoint or 'unknown'
            blueprint = request.blueprint or 'unknown'
            method = request.method
            status = response.status_code
            
            # 记录响应体大小
            response_size = len(response.get_data()) if response.get_data() else 0
            
            # 记录所有指标
            self.REQUEST_COUNT.labels(method, endpoint, status, blueprint).inc()
            self.REQUEST_LATENCY.labels(method, endpoint, blueprint).observe(latency)
            
            if hasattr(g, 'request_size'):
                self.REQUEST_SIZE.labels(method, endpoint, blueprint).observe(g.request_size)
            
            self.RESPONSE_SIZE.labels(method, endpoint, blueprint, status).observe(response_size)
            
            # 调试日志
            if self.debug:
                print(f"完成请求: {method} {request.path} - {status} ({latency:.3f}s)")  # 移除特殊字符
                print(f"    端点: {endpoint}, 蓝图: {blueprint}")
                print(f"    请求大小: {g.request_size} bytes, 响应大小: {response_size} bytes")
        
        except Exception as e:
            if self.debug:
                print(f"记录指标失败: {str(e)}")  # 移除特殊字符
                import traceback
                traceback.print_exc()
        
        return response
    
    def metrics_view(self):
        """指标视图函数"""
        try:
            return Response(generate_latest(REGISTRY), mimetype='text/plain')
        except Exception as e:
            if self.debug:
                print(f"生成指标失败: {str(e)}")  # 移除特殊字符
                import traceback
                traceback.print_exc()
            return Response(f"Error generating metrics: {str(e)}", 500, mimetype='text/plain')