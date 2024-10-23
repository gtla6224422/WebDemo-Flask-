# app/config.py

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://wzd:Wzd123!$&@1.14.155.39:3306/web_demo'
    SECRET_KEY = 'your-secret-key'
    WTF_CSRF_ENABLED = False  # 禁用 CSRF 以便简化示例
    SQLALCHEMY_TRACK_MODIFICATIONS = False