from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
from database import (
    get_all_situations, get_situation_by_id, add_situation,
    update_situation, delete_situation
)
import os

admin_bp = Blueprint('admin', __name__, template_folder='templates')

# Берем логин/пароль из переменных окружения (безопасно для продакшена)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        return render_template('admin/login.html', error='Неверный логин или пароль')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    situations = get_all_situations()
    
    # Группируем ситуации по категориям
    situations_by_category = {}
    for situation in situations:
        category = situation['category']
        if category not in situations_by_category:
            situations_by_category[category] = []
        situations_by_category[category].append(dict(situation))
    
    return render_template('admin/dashboard.html', situations=situations_by_category)

@admin_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_situation_route():
    if request.method == 'POST':
        category = request.form['category']
        title = request.form['title']
        description = request.form['description']
        solution = request.form['solution']
        law = request.form['law']
        status = request.form['status']
        
        add_situation(category, title, description, solution, law, status)
        
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/edit_situation.html')

@admin_bp.route('/edit/<int:situation_id>', methods=['GET', 'POST'])
@login_required
def edit_situation_route(situation_id):
    situation = get_situation_by_id(situation_id)
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        solution = request.form['solution']
        law = request.form['law']
        status = request.form['status']
        
        update_situation(situation_id, title, description, solution, law, status)
        
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/edit_situation.html', situation=situation)

@admin_bp.route('/delete/<int:situation_id>')
@login_required
def delete_situation_route(situation_id):
    delete_situation(situation_id)
    return redirect(url_for('admin.dashboard'))
