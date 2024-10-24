# app/run.py

from app import create_app
import os
import sys

app = create_app()
# 将项目根目录添加到 sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  