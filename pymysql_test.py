import pymysql

# 数据库连接参数
host = '1.14.155.39'
port = 3306
user = 'wzd'
password = 'Wzd123!@#'
database = 'web_demo'

# 尝试连接数据库
try:
    connection = pymysql.connect(host=host,
                                 port=port,
                                 user=user,
                                 password=password,
                                 database=database)
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Failed to connect to the database: {e}")