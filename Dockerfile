# 使用腾讯云的 Python 3.6.8 精简版镜像作为基础镜像
FROM ccr.ccs.tencentyun.com/tencentos/python:3.6.8-slim

# 安装必要的系统依赖
RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到容器的 /app 目录
COPY . /app

# 安装项目依赖，使用国内 PyPI 镜像源
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 暴露 Flask 应用的默认端口
EXPOSE 5000

# 设置环境变量，确保 Flask 在生产环境中运行
ENV FLASK_ENV=production

# 运行 Flask 应用
CMD ["flask", "run", "--host=0.0.0.0"]