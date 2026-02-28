from models.currency_parser import CurrencyParser
from models.currency import CurenciesList
from controllers.databasecontroller import DatabaseController
import json


class CurrencyController:
    def __init__(self):
        self.parser = CurrencyParser()
        self.db = DatabaseController()
        self.selected_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CNY']
        self._currencies_cache = {}
        self._available_cache = None

    def get_current_rates(self):
        """Получить текущие курсы выбранных валют"""
        try:
            currencies = self.parser.get_currencies(self.selected_currencies)
            self._currencies_cache = currencies

            for code, currency in currencies.items():
                self.db.save_currency_history(code, currency.price)

            return currencies
        except Exception as e:
            print(f"Ошибка получения курсов: {e}")
            return self._currencies_cache if self._currencies_cache else {}

    def get_available_currencies(self):
        """Получить список всех доступных валют"""
        if self._available_cache is None:
            try:
                self._available_cache = self.parser.get_all_available_currencies()
            except:
                self._available_cache = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CHF', 'CAD', 'AUD']
        return self._available_cache

    def add_currency(self, currency_code: str):
        """Добавить валюту в отслеживаемые"""
        if currency_code not in self.selected_currencies:
            self.selected_currencies.append(currency_code)
            return True
        return False

    def remove_currency(self, currency_code: str):
        """Удалить валюту из отслеживаемых"""
        if currency_code in self.selected_currencies:
            self.selected_currencies.remove(currency_code)
            return True
        return False

    def update_selected_currencies(self, currencies_list: list):
        """Обновить список отслеживаемых валют"""
        self.selected_currencies = currencies_list

    def get_currency_history(self, currency_code: str, days: int = 90):
        """Получить историю курса валюты"""
        db_history = self.db.get_currency_history(currency_code, days)

        if len(db_history) >= days:
            return db_history

        try:
            api_history = self.parser.get_currency_history(currency_code, days)

            for item in api_history:
                self.db.save_currency_history(currency_code, item["value"])

            return api_history
        except Exception as e:
            print(f"Ошибка получения истории для {currency_code}: {e}")
            return db_history

    def get_currency_history_for_user(self, user_id: int):
        """Получить историю курсов для валют, на которые подписан пользователь"""
        from controllers.usercontroller import UserController
        user_ctrl = UserController()
        user = user_ctrl.get_user(user_id)

        if not user:
            return {}

        history = {}
        for currency_code in user.subscriptions:
            history[currency_code] = self.get_currency_history(currency_code, 30)

        return history

    def refresh_currencies(self):
        """Принудительное обновление курсов"""
        self._currencies_cache = {}
        self._available_cache = None
        return self.get_current_rates()

    def get_currency_info(self, currency_code: str):
        """Получает информацию о конкретной валюте"""
        currencies = self.get_current_rates()
        if currency_code in currencies:
            return currencies[currency_code]

        try:
            return self.parser.get_currency_info(currency_code)
        except:
            return None
