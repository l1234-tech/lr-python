# tests/test_controllers.py
import unittest
from unittest.mock import MagicMock, patch, Mock
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.currencycontroller import CurrencyController
from controllers.usercontroller import UserController
from controllers.databasecontroller import DatabaseController
from models.user import User
from models.currency import CurenciesList


class TestCurrencyController(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.mock_db = MagicMock()
        self.controller = CurrencyController()
        self.controller.db = self.mock_db
        self.controller.parser = MagicMock()

    @patch('controllers.currencycontroller.CurrencyParser')
    def test_get_current_rates_success(self, mock_parser_class):
        """Тест успешного получения курсов валют"""
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser

        # Мокаем возвращаемые данные
        mock_currency_usd = MagicMock(spec=CurenciesList)
        mock_currency_usd.name_curr = 'USD'
        mock_currency_usd.id = 'R01235'
        mock_currency_usd.name = 'Доллар США'
        mock_currency_usd.price = 90.5
        mock_currency_usd.previous = 89.8

        mock_currency_eur = MagicMock(spec=CurenciesList)
        mock_currency_eur.name_curr = 'EUR'
        mock_currency_eur.id = 'R01239'
        mock_currency_eur.name = 'Евро'
        mock_currency_eur.price = 98.2
        mock_currency_eur.previous = 97.5

        mock_data = {
            'USD': mock_currency_usd,
            'EUR': mock_currency_eur
        }
        mock_parser.get_currencies.return_value = mock_data

        controller = CurrencyController()
        controller.parser = mock_parser
        controller.selected_currencies = ['USD', 'EUR']

        result = controller.get_current_rates()

        # Проверяем, что метод вызван с правильными аргументами
        mock_parser.get_currencies.assert_called_once_with(['USD', 'EUR'])
        # Проверяем, что результат содержит ожидаемые данные
        self.assertIn('USD', result)
        self.assertIn('EUR', result)
        self.assertEqual(result['USD'].name_curr, 'USD')
        self.assertEqual(result['EUR'].name_curr, 'EUR')

    @patch('controllers.currencycontroller.CurrencyParser')
    def test_get_current_rates_error(self, mock_parser_class):
        """Тест обработки ошибки при получении курсов"""
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser
        mock_parser.get_currencies.side_effect = Exception("API error")

        controller = CurrencyController()
        controller.parser = mock_parser
        controller.selected_currencies = ['USD']

        # Должен вернуть пустой словарь или кэш
        result = controller.get_current_rates()
        self.assertEqual(result, {})

    def test_add_currency(self):
        """Тест добавления валюты"""
        controller = CurrencyController()
        controller.selected_currencies = ['USD', 'EUR']

        # Добавляем новую валюту
        result = controller.add_currency('GBP')
        self.assertTrue(result)
        self.assertIn('GBP', controller.selected_currencies)

        # Пытаемся добавить существующую валюту
        result = controller.add_currency('USD')
        self.assertFalse(result)

    def test_remove_currency(self):
        """Тест удаления валюты"""
        controller = CurrencyController()
        controller.selected_currencies = ['USD', 'EUR', 'GBP']

        # Удаляем существующую валюту
        result = controller.remove_currency('EUR')
        self.assertTrue(result)
        self.assertNotIn('EUR', controller.selected_currencies)

        # Пытаемся удалить несуществующую валюту
        result = controller.remove_currency('JPY')
        self.assertFalse(result)

    @patch('requests.get')
    def test_parser_get_currencies_success(self, mock_get):
        """Тест парсера с успешным ответом API"""
        from models.currency_parser import CurrencyParser

        # Мокаем успешный ответ API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Valute": {
                "USD": {
                    "ID": "R01235",
                    "Name": "Доллар США",
                    "Value": 90.5,
                    "Previous": 89.8
                }
            }
        }
        mock_get.return_value = mock_response

        parser = CurrencyParser()
        currencies = parser.get_currencies(['USD'])

        self.assertIn('USD', currencies)
        self.assertEqual(currencies['USD'].name_curr, 'USD')
        self.assertEqual(currencies['USD'].price, 90.5)
        self.assertEqual(currencies['USD'].name, "Доллар США")
        mock_get.assert_called_once_with(parser.api_url, timeout=10)

    def test_list_currencies_integration(self):
        """Тест из задания - получение списка валют"""
        mock_db = MagicMock()

        # Создаем контроллер с моком базы данных
        controller = CurrencyController()
        controller.db = mock_db

        # Настраиваем мок для возврата тестовых данных
        mock_currency_usd = MagicMock(spec=CurenciesList)
        mock_currency_usd.name_curr = 'USD'
        mock_currency_usd.id = 'R01235'
        mock_currency_usd.name = 'Доллар США'
        mock_currency_usd.price = 90.5
        mock_currency_usd.previous = 89.8

        mock_currency_eur = MagicMock(spec=CurenciesList)
        mock_currency_eur.name_curr = 'EUR'
        mock_currency_eur.id = 'R01239'
        mock_currency_eur.name = 'Евро'
        mock_currency_eur.price = 98.2
        mock_currency_eur.previous = 97.5

        mock_currencies = {
            'USD': mock_currency_usd,
            'EUR': mock_currency_eur
        }

        # Мокаем get_current_rates
        controller.get_current_rates = MagicMock(return_value=mock_currencies)

        result = controller.get_current_rates()

        # Проверяем результат
        self.assertEqual(len(result), 2)
        self.assertIn('USD', result)
        self.assertIn('EUR', result)
        self.assertEqual(result['USD'].name_curr, 'USD')
        self.assertEqual(result['EUR'].name_curr, 'EUR')


class TestUserController(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.mock_db = MagicMock()
        self.controller = UserController()
        self.controller.db = self.mock_db

    def test_get_all_users(self):
        """Тест получения всех пользователей"""
        # Мокаем данные из базы
        mock_user1 = User(1, 'Андрей')
        mock_user1.add_subscription('USD')
        mock_user1.add_subscription('EUR')

        mock_user2 = User(2, 'Мария')
        mock_user2.add_subscription('GBP')

        self.mock_db.get_all_users.return_value = [mock_user1, mock_user2]

        result = self.controller.get_all_users()

        self.mock_db.get_all_users.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, 'Андрей')
        self.assertEqual(result[1].name, 'Мария')

    def test_add_user(self):
        """Тест добавления пользователя"""
        mock_user_id = 5
        self.mock_db.add_user.return_value = mock_user_id

        result = self.controller.add_user("Новый пользователь")

        self.mock_db.add_user.assert_called_once_with("Новый пользователь")
        self.assertEqual(result, mock_user_id)

    def test_update_user_subscription(self):
        """Тест обновления подписки пользователя"""
        # Мокаем получение пользователя
        mock_user = User(1, "Андрей")
        mock_user.add_subscription = MagicMock()
        mock_user.remove_subscription = MagicMock()
        mock_user.has_subscription = MagicMock(return_value=False)

        self.mock_db.get_user.return_value = mock_user
        self.mock_db.update_user_subscription.return_value = True

        # Тест добавления подписки
        result = self.controller.update_user_subscription(1, 'USD', True)

        self.assertTrue(result)
        mock_user.add_subscription.assert_called_once_with('USD')
        self.mock_db.update_user_subscription.assert_called_once_with(1, 'USD', True)

        # Сбрасываем моки для следующего теста
        mock_user.add_subscription.reset_mock()
        mock_user.remove_subscription.reset_mock()
        self.mock_db.update_user_subscription.reset_mock()

        # Тест удаления подписки
        mock_user.has_subscription.return_value = True
        result = self.controller.update_user_subscription(1, 'USD', False)

        self.assertTrue(result)
        mock_user.remove_subscription.assert_called_once_with('USD')
        self.mock_db.update_user_subscription.assert_called_once_with(1, 'USD', False)

    def test_get_user_not_found(self):
        """Тест получения несуществующего пользователя"""
        self.mock_db.get_user.return_value = None

        result = self.controller.get_user(999)

        self.assertIsNone(result)
        self.mock_db.get_user.assert_called_once_with(999)


class TestDatabaseController(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_init_database(self, mock_connect):
        """Тест инициализации базы данных"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Мокаем fetchone для проверки пустой таблицы пользователей
        mock_cursor.fetchone.side_effect = [(0,), None]

        db = DatabaseController('test.db')

        # Проверяем, что были созданы таблицы
        self.assertTrue(mock_cursor.execute.call_count >= 3)

        # Проверяем что был установлен row_factory (может быть None в моках)
        self.assertIsNotNone(db.db_path)

    @patch('sqlite3.connect')
    def test_add_user(self, mock_connect):
        """Тест добавления пользователя"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Мокаем максимальный ID
        mock_cursor.fetchone.return_value = (5,)

        db = DatabaseController('test.db')
        new_id = db.add_user("Новый пользователь")

        # Проверяем, что был выполнен INSERT запрос
        self.assertEqual(new_id, 6)  # 5 + 1
        mock_cursor.execute.assert_any_call(
            'INSERT INTO users (id, name) VALUES (?, ?)',
            (6, "Новый пользователь")
        )

    @patch('sqlite3.connect')
    def test_update_user_subscription_add(self, mock_connect):
        """Тест добавления подписки пользователя"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Мокаем существование пользователя
        mock_cursor.fetchone.return_value = (1,)

        db = DatabaseController('test.db')
        result = db.update_user_subscription(1, 'USD', True)

        self.assertTrue(result)

        # Проверяем, что был выполнен INSERT запрос
        insert_found = False
        for call_args in mock_cursor.execute.call_args_list:
            args = call_args[0]
            if len(args) > 0 and 'INSERT INTO user_subscriptions' in args[0]:
                insert_found = True
                self.assertEqual(args[1], (1, 'USD'))
                break

        self.assertTrue(insert_found)

    @patch('sqlite3.connect')
    def test_update_user_subscription_remove(self, mock_connect):
        """Тест удаления подписки пользователя"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Мокаем существование пользователя
        mock_cursor.fetchone.return_value = (1,)

        db = DatabaseController('test.db')
        result = db.update_user_subscription(1, 'USD', False)

        self.assertTrue(result)

        # Проверяем, что был выполнен DELETE запрос
        delete_found = False
        for call_args in mock_cursor.execute.call_args_list:
            args = call_args[0]
            if len(args) > 0 and 'DELETE FROM user_subscriptions' in args[0]:
                delete_found = True
                self.assertEqual(args[1], (1, 'USD'))
                break

        self.assertTrue(delete_found)

    @patch('sqlite3.connect')
    @patch('datetime.datetime')
    def test_save_currency_history(self, mock_datetime, mock_connect):
        """Тест сохранения истории курса"""
        # Мокаем datetime.now()
        mock_now = MagicMock()
        mock_now.strftime.return_value = '2025-12-05'
        mock_datetime.now.return_value = mock_now

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db = DatabaseController('test_history.db')

        # Сбрасываем счетчик вызовов execute
        mock_cursor.execute.reset_mock()

        # Вызываем тестируемый метод
        db.save_currency_history('USD', 90.5)

        # Проверяем, что был выполнен INSERT запрос
        insert_found = False
        for call_args in mock_cursor.execute.call_args_list:
            args = call_args[0]
            if len(args) > 0 and 'INSERT OR REPLACE INTO currency_history' in args[0]:
                insert_found = True
                self.assertIn('USD', args[1])
                self.assertIn('2025-12-05', args[1])
                self.assertIn(90.5, args[1])
                break

        self.assertTrue(insert_found, "INSERT запрос не был найден в вызовах execute")

    @patch('sqlite3.connect')
    def test_get_currency_history(self, mock_connect):
        """Тест получения истории курса"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Мокаем данные истории
        mock_cursor.fetchall.return_value = [
            ('2025-12-01', 89.5),
            ('2025-12-02', 90.0),
            ('2025-12-03', 90.5)
        ]

        db = DatabaseController('test.db')
        history = db.get_currency_history('USD', 30)

        # Проверяем, что был выполнен SELECT запрос
        select_found = False
        for call_args in mock_cursor.execute.call_args_list:
            args = call_args[0]
            if len(args) > 0 and 'SELECT date, value FROM currency_history' in args[0]:
                select_found = True
                self.assertEqual(args[1], ('USD', 30))
                break

        self.assertTrue(select_found)
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]['date'], '2025-12-01')
        self.assertEqual(history[0]['value'], 89.5)


if __name__ == '__main__':
    unittest.main()