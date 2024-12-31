# app/run.py
# coding=utf-8

from app import create_app
from prometheus_client import Counter, Histogram, start_http_server
from flask import Flask, request
import time
import os
import sys

app = create_app()
# 将项目根目录添加到 sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == '__main__':
    start_http_server(5002)
    app.run(host='0.0.0.0', port=5001, debug=True)  