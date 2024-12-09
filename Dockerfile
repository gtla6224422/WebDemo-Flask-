# 使用阿里云的 Python 3.9 精简版镜像作为基础镜像
FROM registry.cn-hangzhou.aliyuncs.com/library/python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到容器的 /app 目录
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 应用的默认端口
EXPOSE 5003

# 设置环境变量，确保 Flask 在生产环境中运行
ENV FLASK_ENV=production

# 运行 Flask 应用
CMD ["flask", "run", "--host=0.0.0.0"]