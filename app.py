from flask import Flask, render_template, session, request, redirect, url_for
from admin import admin_bp
from database import init_db, get_situations_by_category, insert_initial_data

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-please-change-it-for-production'

# Регистрируем blueprint админки
app.register_blueprint(admin_bp, url_prefix='/admin')

# Инициализируем базу данных при запуске
def initialize_database():
    """Инициализация БД и добавление начальных данных"""
    init_db()
    # Добавляем начальные данные (только если их нет)
    try:
        insert_initial_data()
        print("База данных инициализирована с начальными данными")
    except Exception as e:
        print(f"Ошибка при инициализации данных: {e}")

# Вызываем инициализацию
initialize_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/zhkh')
def zhkh():
    situations = get_situations_by_category('zhkh')
    return render_template('zhkh.html', situations=situations)

@app.route('/family')
def family():
    situations = get_situations_by_category('family')
    return render_template('family.html', situations=situations)

@app.route('/labor')
def labor():
    situations = get_situations_by_category('labor')
    return render_template('labor.html', situations=situations)

@app.route('/dtp')
def dtp():
    situations = get_situations_by_category('dtp')
    return render_template('dtp.html', situations=situations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)