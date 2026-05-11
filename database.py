import sqlite3
from contextlib import contextmanager

DATABASE_PATH = 'legal_help.db'

# Начальные данные перенесены сюда
INITIAL_SITUATIONS = {
    'zhkh': [
        {
            'id': 1,
            'title': 'Залив соседями',
            'description': 'Соседи сверху затопили квартиру, отказываются возмещать ущерб',
            'solution': '1. Составьте акт с УК\n2. Оцените ущерб\n3. Направьте претензию\n4. Подайте иск в суд',
            'law': 'Ст. 1064 ГК РФ',
            'status': 'active'
        },
        {
            'id': 2,
            'title': 'Перерасчет ЖКУ',
            'description': 'УК отказывается делать перерасчет за время отсутствия',
            'solution': 'Подайте заявление с подтверждающими документами',
            'law': 'Постановление Правительства РФ №354',
            'status': 'active'
        }
    ],
    'family': [
        {
            'id': 3,
            'title': 'Развод и раздел имущества',
            'description': 'Супруга подала на развод, не можем договориться о разделе квартиры',
            'solution': 'Заключите соглашение или обращайтесь в суд',
            'law': 'Ст. 38 СК РФ',
            'status': 'active'
        },
        {
            'id': 6,
            'title': 'Взыскание алиментов',
            'description': 'Бывший супруг не платит алименты на ребенка',
            'solution': '1. Обратитесь к приставам\n2. Подайте иск в суд о взыскании задолженности\n3. Требуйте привлечения к административной ответственности',
            'law': 'Ст. 80 СК РФ',
            'status': 'active'
        }
    ],
    'labor': [
        {
            'id': 4,
            'title': 'Невыплата зарплаты',
            'description': 'Работодатель задерживает зарплату на 2 месяца',
            'solution': '1. Жалоба в трудовую инспекцию\n2. Заявление в прокуратуру\n3. Иск в суд',
            'law': 'Ст. 236 ТК РФ',
            'status': 'active'
        },
        {
            'id': 7,
            'title': 'Незаконное увольнение',
            'description': 'Уволили по сокращению, но не предложили другие вакансии',
            'solution': 'Обжалуйте увольнение в суде в течение 1 месяца',
            'law': 'Ст. 81 ТК РФ',
            'status': 'active'
        }
    ],
    'dtp': [
        {
            'id': 5,
            'title': 'ОСАГО не покрывает ущерб',
            'description': 'Страховая выплатила меньше стоимости ремонта',
            'solution': 'Закажите независимую экспертизу и подайте претензию',
            'law': 'ФЗ Об ОСАГО',
            'status': 'active'
        },
        {
            'id': 8,
            'title': 'Оформление ДТП без ГИБДД',
            'description': 'Можно ли оформить европротокол при разногласиях',
            'solution': 'Если есть разногласия, вызывайте ГИБДД. Европротокол только при согласии',
            'law': 'Ст. 11.1 ФЗ Об ОСАГО',
            'status': 'active'
        }
    ]
}

@contextmanager
def get_db_connection():
    """Контекстный менеджер для работы с базой данных"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Инициализация базы данных и создание таблиц"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS situations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                solution TEXT NOT NULL,
                law TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()

def add_situation(category, title, description, solution, law, status='active'):
    """Добавление новой ситуации"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO situations (category, title, description, solution, law, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (category, title, description, solution, law, status))
        conn.commit()
        return cursor.lastrowid

def get_situations_by_category(category):
    """Получение всех ситуаций по категории"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM situations 
            WHERE category = ? AND status = 'active'
            ORDER BY id DESC
        ''', (category,))
        return cursor.fetchall()

def get_all_situations():
    """Получение всех ситуаций (для админки)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM situations 
            ORDER BY category, id DESC
        ''')
        return cursor.fetchall()

def get_situation_by_id(situation_id):
    """Получение ситуации по ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM situations WHERE id = ?', (situation_id,))
        return cursor.fetchone()

def update_situation(situation_id, title, description, solution, law, status):
    """Обновление ситуации"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE situations 
            SET title = ?, description = ?, solution = ?, law = ?, status = ?, 
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, description, solution, law, status, situation_id))
        conn.commit()
        return cursor.rowcount > 0

def delete_situation(situation_id):
    """Удаление ситуации"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM situations WHERE id = ?', (situation_id,))
        conn.commit()
        return cursor.rowcount > 0

def get_categories_count():
    """Получение количества ситуаций по категориям"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM situations 
            WHERE status = 'active'
            GROUP BY category
        ''')
        return {row['category']: row['count'] for row in cursor.fetchall()}

def insert_initial_data():
    """Вставка начальных данных из INITIAL_SITUATIONS"""
    for category, situations in INITIAL_SITUATIONS.items():
        for situation in situations:
            # Проверяем, есть ли уже такая ситуация по заголовку
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id FROM situations 
                    WHERE category = ? AND title = ?
                ''', (category, situation['title']))
                existing = cursor.fetchone()
            
            if not existing:
                add_situation(
                    category=category,
                    title=situation['title'],
                    description=situation['description'],
                    solution=situation['solution'],
                    law=situation['law'],
                    status=situation.get('status', 'active')
                )
                print(f"Добавлена ситуация: {situation['title']}")