import sqlite3
from controllers.databasecontroller import DatabaseController
from models.user import User


class UserController:
    def __init__(self):
        self.db = DatabaseController()
        self._init_test_users()

    def _init_test_users(self):
        """Инициализация тестовых пользователей"""
        users = self.db.get_all_users()
        if not users:
            user_ids = []
            user_ids.append(self.db.add_user("Андрей"))
            user_ids.append(self.db.add_user("Мария"))
            user_ids.append(self.db.add_user("Иван"))

            for user_id in user_ids:
                if user_id == user_ids[0]:  
                    self.db.update_user_subscription(user_id, 'USD', True)
                    self.db.update_user_subscription(user_id, 'EUR', True)
                elif user_id == user_ids[1]:  
                    self.db.update_user_subscription(user_id, 'GBP', True)
                    self.db.update_user_subscription(user_id, 'JPY', True)
                elif user_id == user_ids[2]:  
                    self.db.update_user_subscription(user_id, 'CNY', True)

            print("Тестовые пользователи и подписки созданы")

    def get_all_users(self):
        """Получить всех пользователей"""
        return self.db.get_all_users()

    def get_user(self, user_id: int):
        """Получить пользователя по ID"""
        return self.db.get_user(user_id)

    def add_user(self, name: str):
        """Добавить нового пользователя"""
        return self.db.add_user(name)

    def update_user_subscription(self, user_id: int, currency_code: str, subscribe: bool):
        """Обновить подписку пользователя - ИСПРАВЛЕННЫЙ МЕТОД"""
        user = self.get_user(user_id)
        if not user:
            return False

        success = False
        if subscribe:
            if not user.has_subscription(currency_code):
                user.add_subscription(currency_code)
                success = True
        else:
            if user.has_subscription(currency_code):
                user.remove_subscription(currency_code)
                success = True

        if success:
            self.db.update_user_subscription(user_id, currency_code, subscribe)

        return success

    def delete_user(self, user_id: int):
        """Удалить пользователя"""
        return self.db.delete_user(user_id)

    def get_user_subscriptions(self, user_id: int):
        """Получить подписки пользователя"""
        user = self.get_user(user_id)
        if user:
            return user.subscriptions
        return []

    def get_users_count(self):
        """Получить количество пользователей"""
        users = self.get_all_users()
        return len(users) if users else 0

    def get_total_subscriptions_count(self):
        """Получить общее количество подписок"""
        users = self.get_all_users()
        total = 0
        if users:
            for user in users:
                total += len(user.subscriptions)
        return total

    def update_user_subscriptions(self, user_id: int, subscriptions: list):
        """Обновить все подписки пользователя"""
        user = self.get_user(user_id)
        if not user:
            return False

        current_subs = set(user.subscriptions)
        new_subs = set(subscriptions)

        for currency_code in new_subs - current_subs:
            self.update_user_subscription(user_id, currency_code, True)

        for currency_code in current_subs - new_subs:
            self.update_user_subscription(user_id, currency_code, False)

        return True
