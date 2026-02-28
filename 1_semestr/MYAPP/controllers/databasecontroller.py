import sqlite3
from datetime import datetime
from models import User


class DatabaseController:
    def __init__(self, db_path: str = 'currencies.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Инициализация базы данных с таблицами"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_subscriptions (
                    user_id INTEGER,
                    currency_code TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    PRIMARY KEY(user_id, currency_code)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS currency_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    currency_code TEXT,
                    date DATE,
                    value REAL,
                    UNIQUE(currency_code, date)
                )
            ''')

            cursor.execute('SELECT COUNT(*) FROM users')
            if cursor.fetchone()[0] == 0:
                cursor.execute('INSERT INTO users (id, name) VALUES (1, "Андрей")')
                cursor.execute('INSERT INTO users (id, name) VALUES (2, "Мария")')
                cursor.execute('INSERT INTO users (id, name) VALUES (3, "Иван")')

            conn.commit()

    def get_all_users(self):
        """Получить всех пользователей"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM users ORDER BY id')
            rows = cursor.fetchall()

            users = []
            for row in rows:
                user = User(row['id'], row['name'])
                cursor.execute('SELECT currency_code FROM user_subscriptions WHERE user_id = ?', (row['id'],))
                subscriptions = [row[0] for row in cursor.fetchall()]
                for sub in subscriptions:
                    user.add_subscription(sub)
                users.append(user)

            return users

    def get_user(self, user_id: int):
        """Получить пользователя по ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()

            if row:
                user = User(row['id'], row['name'])
                cursor.execute('SELECT currency_code FROM user_subscriptions WHERE user_id = ?', (user_id,))
                subscriptions = [row[0] for row in cursor.fetchall()]
                for sub in subscriptions:
                    user.add_subscription(sub)
                return user
            return None

    def add_user(self, name: str):
        """Добавить нового пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT MAX(id) FROM users')
            max_id = cursor.fetchone()[0] or 0
            new_id = max_id + 1

            cursor.execute('INSERT INTO users (id, name) VALUES (?, ?)', (new_id, name))
            conn.commit()
            return new_id

    def update_user_subscription(self, user_id: int, currency_code: str, subscribe: bool):
        """Обновить подписку пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
            if not cursor.fetchone():
                return False

            if subscribe:
                try:
                    cursor.execute('''
                        INSERT INTO user_subscriptions (user_id, currency_code) 
                        VALUES (?, ?)
                    ''', (user_id, currency_code))
                except sqlite3.IntegrityError:
                    pass
            else:
                cursor.execute('''
                    DELETE FROM user_subscriptions 
                    WHERE user_id = ? AND currency_code = ?
                ''', (user_id, currency_code))

            conn.commit()
            return True

    def delete_user(self, user_id: int):
        """Удалить пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM user_subscriptions WHERE user_id = ?', (user_id,))
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            return cursor.rowcount > 0

    def save_currency_history(self, currency_code: str, value: float):
        """Сохранить историю курса валюты"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            today = datetime.now().strftime('%Y-%m-%d')

            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO currency_history (currency_code, date, value)
                    VALUES (?, ?, ?)
                ''', (currency_code, today, value))
                conn.commit()
            except Exception as e:
                print(f"Ошибка сохранения истории: {e}")

    def get_currency_history(self, currency_code: str, days: int = 90):
        """Получить историю курса валюты"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT date, value FROM currency_history 
                WHERE currency_code = ? 
                ORDER BY date DESC 
                LIMIT ?
            ''', (currency_code, days))

            rows = cursor.fetchall()
            history = []
            for row in rows:
                history.append({"date": row[0], "value": row[1]})

            if not history:
                cursor.execute('''
                    SELECT value FROM currency_history 
                    WHERE currency_code = ? 
                    ORDER BY date DESC 
                    LIMIT 1
                ''', (currency_code,))
                last_value = cursor.fetchone()
                if last_value:
                    history.append({"date": datetime.now().strftime('%Y-%m-%d'), "value": last_value[0]})

            return history

    def update_user_subscriptions(self, user_id: int, subscriptions: list):
        """Обновить все подписки пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('DELETE FROM user_subscriptions WHERE user_id = ?', (user_id,))

            for currency_code in subscriptions:
                cursor.execute('''
                    INSERT INTO user_subscriptions (user_id, currency_code) 
                    VALUES (?, ?)
                ''', (user_id, currency_code))

            conn.commit()
            return True
