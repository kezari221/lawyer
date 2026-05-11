from flask import Flask, render_template
from admin import admin_bp
from database import init_db, get_situations_by_category, insert_initial_data
import os

app = Flask(__name__)
# Берем секретный ключ из переменных окружения (для Render.com)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-for-development')

# Регистрируем blueprint админки
app.register_blueprint(admin_bp, url_prefix='/admin')

# Инициализируем базу данных при запуске
def initialize_database():
    """Инициализация БД и добавление начальных данных"""
    try:
        init_db()
        print("База данных инициализирована")
        
        # Добавляем начальные данные
        insert_initial_data()
        print("Начальные данные успешно добавлены")
        
    except Exception as e:
        print(f"Ошибка при инициализации: {e}")

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
