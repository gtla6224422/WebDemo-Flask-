import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://wzd:Wzd123!$&@1.14.155.39:3306/web_demo'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['WTF_CSRF_ENABLED'] = False  # 禁用 CSRF 以便简化示例

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# 初始化 Flask-Migrate
migrate = Migrate(app, db)


# 用户模型
class User(db.Model):
    __tablename__ = 'user_tbl'  # 显式指定表名为 user_tbl
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Integer, default=1)
    user_status = db.Column(db.Integer, default=1)
    create_time = db.Column(db.TIMESTAMP, server_default=func.now())  # 添加 create_time 字段，默认值为当前时间戳
    last_update_time = db.Column(db.TIMESTAMP, server_default=func.now())  # 添加 create_time 字段，默认值为当前时间戳

    
# 登录表单
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=255)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=255)])
    submit = SubmitField('Login')

# 注册表单
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=255)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=255)])
    submit = SubmitField('Register')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)