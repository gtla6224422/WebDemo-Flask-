FROM python:3.6.8 

# 设置工作目录
WORKDIR /

# 将应用代码复制到运行时容器
COPY . /

RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 应用的默认端口
EXPOSE 5003

# 运行 Flask 应用
CMD ["flask", "run", "--host=0.0.0.0"]