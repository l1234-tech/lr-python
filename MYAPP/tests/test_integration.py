# tests/test_integration.py
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestPagesController(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом"""
        from jinja2 import Environment, DictLoader

        # Создаем мок окружения Jinja2
        self.mock_env = MagicMock(spec=Environment)

        # Импортируем PagesController после настройки sys.path
        from controllers.pages import PagesController
        self.pages_ctrl = PagesController(self.mock_env)

        # Мокаем контроллеры
        self.pages_ctrl.currency_ctrl = MagicMock()
        self.pages_ctrl.user_ctrl = MagicMock()

    def test_render_index(self):
        """Тест рендеринга главной страницы"""
        # Мокаем данные
        mock_currency_usd = MagicMock()
        mock_currency_usd.name = 'Доллар США'
        mock_currency_usd.name_curr = 'USD'
        mock_currency_usd.price = 90.5
        mock_currency_usd.previous = 89.8

        mock_currency_eur = MagicMock()
        mock_currency_eur.name = 'Евро'
        mock_currency_eur.name_curr = 'EUR'
        mock_currency_eur.price = 98.2
        mock_currency_eur.previous = 97.5

        mock_currencies = {
            'USD': mock_currency_usd,
            'EUR': mock_currency_eur
        }
        self.pages_ctrl.currency_ctrl.get_current_rates.return_value = mock_currencies

        # Мокаем шаблон
        mock_template = MagicMock()
        self.mock_env.get_template.return_value = mock_template

        # Вызываем метод
        self.pages_ctrl.render_index()

        # Проверяем, что был вызван правильный шаблон
        self.mock_env.get_template.assert_called_once_with("index.html")

        # Проверяем, что render был вызван с правильными аргументами
        mock_template.render.assert_called_once()

    def test_render_user_success(self):
        """Тест рендеринга страницы пользователя (успешный)"""
        # Мокаем пользователя
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.name = "Андрей"
        mock_user.subscriptions = ['USD', 'EUR']
        self.pages_ctrl.user_ctrl.get_user.return_value = mock_user

        # Мокаем доступные валюты
        self.pages_ctrl.currency_ctrl.get_available_currencies.return_value = ['USD', 'EUR', 'GBP']

        # Мокаем данные валют
        mock_currency_usd = MagicMock()
        mock_currency_usd.name_curr = 'USD'
        mock_currency_usd.name = 'Доллар США'
        mock_currency_usd.price = 90.5
        mock_currency_usd.previous = 89.8

        mock_currency_eur = MagicMock()
        mock_currency_eur.name_curr = 'EUR'
        mock_currency_eur.name = 'Евро'
        mock_currency_eur.price = 98.2
        mock_currency_eur.previous = 97.5

        def get_currency_info_side_effect(code):
            if code == 'USD':
                return mock_currency_usd
            elif code == 'EUR':
                return mock_currency_eur
            return None

        self.pages_ctrl.currency_ctrl.get_currency_info.side_effect = get_currency_info_side_effect

        # Мокаем историю
        self.pages_ctrl.currency_ctrl.get_currency_history.return_value = [
            {"date": "2024-01-01", "value": 89.0},
            {"date": "2024-01-02", "value": 90.0}
        ]

        # Мокаем шаблон
        mock_template = MagicMock()
        self.mock_env.get_template.return_value = mock_template

        # Вызываем метод
        self.pages_ctrl.render_user(1)

        # Проверяем вызовы
        self.pages_ctrl.user_ctrl.get_user.assert_called_once_with(1)
        self.mock_env.get_template.assert_called_once_with("user.html")
        mock_template.render.assert_called_once()

    def test_render_user_not_found(self):
        """Тест рендеринга страницы пользователя (не найден)"""
        self.pages_ctrl.user_ctrl.get_user.return_value = None

        # Мокаем шаблон для ошибки
        mock_template = MagicMock()
        self.mock_env.get_template.return_value = mock_template

        result = self.pages_ctrl.render_user(999)

        # Должен вернуться результат рендеринга ошибки
        self.assertEqual(result, mock_template.render.return_value)
        mock_template.render.assert_called_once()

    def test_render_currencies(self):
        """Тест рендеринга страницы валют"""
        # Мокаем данные
        mock_currency_usd = MagicMock()
        mock_currency_usd.name = 'Доллар США'
        mock_currency_usd.name_curr = 'USD'
        mock_currency_usd.price = 90.5
        mock_currency_usd.previous = 89.8

        mock_currency_eur = MagicMock()
        mock_currency_eur.name = 'Евро'
        mock_currency_eur.name_curr = 'EUR'
        mock_currency_eur.price = 98.2
        mock_currency_eur.previous = 97.5

        mock_currencies = {
            'USD': mock_currency_usd,
            'EUR': mock_currency_eur
        }
        self.pages_ctrl.currency_ctrl.get_current_rates.return_value = mock_currencies

        # Мокаем доступные валюты
        self.pages_ctrl.currency_ctrl.get_available_currencies.return_value = ['USD', 'EUR', 'GBP', 'JPY']
        self.pages_ctrl.currency_ctrl.selected_currencies = ['USD', 'EUR']

        # Мокаем шаблон
        mock_template = MagicMock()
        self.mock_env.get_template.return_value = mock_template

        # Вызываем метод
        self.pages_ctrl.render_currencies()

        # Проверяем
        self.mock_env.get_template.assert_called_once_with("currencies.html")
        mock_template.render.assert_called_once()

    def test_render_author(self):
        """Тест рендеринга страницы об авторе"""
        mock_template = MagicMock()
        self.mock_env.get_template.return_value = mock_template

        self.pages_ctrl.render_author()

        self.mock_env.get_template.assert_called_once_with("author.html")
        mock_template.render.assert_called_once()


if __name__ == '__main__':
    unittest.main()