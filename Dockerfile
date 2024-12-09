# 第一阶段：构建阶段
FROM python:3.6.8 AS builder

# 安装必要的系统依赖
RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /

# 将当前目录下的所有文件复制到容器的 /app 目录
COPY . /

# 安装项目依赖，使用国内 PyPI 镜像源
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 第二阶段：运行阶段
FROM ccr.ccs.tencentyun.com/tencentos/python:3.6.8-slim

# 设置工作目录
WORKDIR /

# 从构建阶段复制安装好的依赖
COPY --from=builder /usr/local/lib/python3.6/site-packages /usr/local/lib/python3.6/site-packages

# 将应用代码复制到运行时容器
COPY . /

# 暴露 Flask 应用的默认端口
EXPOSE 5003

# 设置环境变量，确保 Flask 在生产环境中运行
ENV FLASK_ENV=production

# 运行 Flask 应用
CMD ["flask", "run", "--host=0.0.0.0"]