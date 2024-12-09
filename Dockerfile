# 第一阶段：构建阶段
FROM python:3.6.8 

# 设置工作目录
WORKDIR /

# 将应用代码复制到运行时容器
COPY . /

# 暴露 Flask 应用的默认端口
EXPOSE 5003

# 运行 Flask 应用
CMD ["flask", "run", "--host=0.0.0.0"]