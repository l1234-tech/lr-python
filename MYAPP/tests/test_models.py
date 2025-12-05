# tests/test_models.py
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user import User
from models.currency import CurenciesList
from models.author import Author


class TestUserModel(unittest.TestCase):

    def test_user_creation(self):
        """Тест создания пользователя"""
        user = User(1, "Андрей")

        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Андрей")
        self.assertEqual(user.subscriptions, [])

    def test_user_setter_validation(self):
        """Тест валидации сеттеров"""
        user = User(1, "Андрей")

        # Корректное имя
        user.name = "Мария"
        self.assertEqual(user.name, "Мария")

        # Некорректное имя (должно вызвать исключение)
        with self.assertRaises(ValueError) as context:
            user.name = ""
        self.assertEqual(str(context.exception), "Имя не может быть меньше одного символа")

        # Некорректный ID (должно вызвать исключение)
        with self.assertRaises(ValueError) as context:
            user.id = -1
        self.assertEqual(str(context.exception), "ID должно быть положительным числом")

    def test_subscription_management(self):
        """Тест управления подписками"""
        user = User(1, "Андрей")

        # Добавление подписки
        result = user.add_subscription("USD")
        self.assertTrue(result)
        self.assertIn("USD", user.subscriptions)

        # Добавление дублирующей подписки
        result = user.add_subscription("USD")
        self.assertFalse(result)

        # Проверка наличия подписки
        self.assertTrue(user.has_subscription("USD"))
        self.assertFalse(user.has_subscription("EUR"))

        # Удаление подписки
        result = user.remove_subscription("USD")
        self.assertTrue(result)
        self.assertNotIn("USD", user.subscriptions)

        # Удаление несуществующей подписки
        result = user.remove_subscription("EUR")
        self.assertFalse(result)

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        user = User(1, "Андрей")
        user.add_subscription("USD")
        user.add_subscription("EUR")

        result = user.to_dict()

        self.assertEqual(result['id'], 1)
        self.assertEqual(result['name'], "Андрей")
        self.assertEqual(result['subscriptions'], ["USD", "EUR"])
        self.assertEqual(result['subscriptions_count'], 2)


class TestCurrencyModel(unittest.TestCase):

    def test_currency_creation(self):
        """Тест создания валюты"""
        currency = CurenciesList("USD", "R01235", "Доллар США", 90.5, 89.8)

        self.assertEqual(currency.name_curr, "USD")
        self.assertEqual(currency.id, "R01235")
        self.assertEqual(currency.name, "Доллар США")
        self.assertEqual(currency.price, 90.5)
        self.assertEqual(currency.previous, 89.8)

    def test_currency_properties(self):
        """Тест свойств валюты"""
        currency = CurenciesList("USD", "R01235", "Доллар США", 90.5, 89.8)

        # Проверяем все свойства
        self.assertEqual(currency.name_curr, "USD")
        self.assertEqual(currency.id, "R01235")
        self.assertEqual(currency.price, 90.5)
        self.assertEqual(currency.name, "Доллар США")
        self.assertEqual(currency.previous, 89.8)

    def test_currency_setter_validation(self):
        """Тест валидации сеттеров валюты"""
        currency = CurenciesList("USD", "R01235", "Доллар США", 90.5, 89.8)

        # Корректный код валюты
        currency.name_curr = "EUR"
        self.assertEqual(currency.name_curr, "EUR")

        # Некорректный код валюты (должно вызвать исключение)
        with self.assertRaises(ValueError) as context:
            currency.name_curr = "EURO"
        self.assertEqual(str(context.exception), "Имя валюты должно содержать 3 символа")

        # Некорректная цена (должно вызвать исключение)
        with self.assertRaises(ValueError) as context:
            currency.price = -10
        self.assertEqual(str(context.exception), "Цена должна быть положительным числом")

    def test_to_dict(self):
        """Тест преобразования валюты в словарь"""
        currency = CurenciesList("USD", "R01235", "Доллар США", 90.5, 89.8)

        result = currency.to_dict()

        self.assertEqual(result['name_curr'], "USD")
        self.assertEqual(result['id'], "R01235")
        self.assertEqual(result['name'], "Доллар США")
        self.assertEqual(result['price'], 90.5)
        self.assertEqual(result['previous'], 89.8)

    def test_str_representation(self):
        """Тест строкового представления"""
        currency = CurenciesList("USD", "R01235", "Доллар США", 90.5, 89.8)

        result = str(currency)
        self.assertIn("USD", result)
        self.assertIn("90.5000", result)

    def test_repr_representation(self):
        """Тест представления repr"""
        currency = CurenciesList("USD", "R01235", "Доллар США", 90.5, 89.8)

        result = repr(currency)
        self.assertIn("Currency", result)
        self.assertIn("USD", result)
        self.assertIn("90.5", result)


class TestAuthorModel(unittest.TestCase):

    def test_author_creation(self):
        """Тест создания автора"""
        author = Author("Сырчин Андрей", "P3122")

        self.assertEqual(author.name, "Сырчин Андрей")
        self.assertEqual(author.group, "P3122")

    def test_author_setter_validation(self):
        """Тест валидации сеттеров автора"""
        author = Author("Сырчин Андрей", "P3122")

        # Корректное имя
        author.name = "Иванов Иван"
        self.assertEqual(author.name, "Иванов Иван")

        # Некорректное имя (должно вызвать исключение)
        with self.assertRaises(ValueError) as context:
            author.name = ""
        self.assertEqual(str(context.exception), "Имя не может быть меньше одного символа")

        # Некорректная группа (должно вызвать исключение)
        with self.assertRaises(ValueError) as context:
            author.group = "P312"
        self.assertEqual(str(context.exception), "Группа должна быть 5 символов длиной")

    def test_to_dict(self):
        """Тест преобразования автора в словарь"""
        author = Author("Сырчин Андрей", "P3122")

        result = author.to_dict()

        self.assertEqual(result['name'], "Сырчин Андрей")
        self.assertEqual(result['group'], "P3122")


if __name__ == '__main__':
    unittest.main()