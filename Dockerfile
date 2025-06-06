FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . .

EXPOSE 5003

CMD ["flask", "run", "--host=0.0.0.0", "--port=5003"]
