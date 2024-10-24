# app/views.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from .model import models  # 导入 models 模块
from .form.forms import LoginForm, RegisterForm
from flask_bcrypt import Bcrypt

# 创建蓝图
login_bp = Blueprint('login_bp', __name__)

bcrypt = Bcrypt()

@login_bp.route('/')
def index():
    return render_template('index.html')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html', form=form)

@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = models.User(username=form.username.data, password=hashed_password)
        models.db.session.add(new_user)
        models.db.session.commit()
        flash('Registration successful.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)