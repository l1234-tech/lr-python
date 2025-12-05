import io
import unittest
import requests
import json
from unittest.mock import patch, Mock
from main import logger, get_currencies

class TestGetCurrenciesFunction(unittest.TestCase):
    def test_correct_currency_return(self):
        with patch('main.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "Valute": {
                    "USD": {"Value": 93.25},
                    "EUR": {"Value": 101.7}
                }
            }
            mock_get.return_value = mock_response

            result = get_currencies(['USD', 'EUR'])

            self.assertIsInstance(result, dict)
            self.assertEqual(len(result), 2)
            self.assertIn('USD', result)
            self.assertIn('EUR', result)
            self.assertEqual(result['USD'], 93.25)
            self.assertEqual(result['EUR'], 101.7)
            self.assertIsInstance(result['USD'], float)
            self.assertIsInstance(result['EUR'], float)

    def test_non_exist_currency(self):
        with patch('main.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "Valute": {
                    "USD": {"Value": 93.25}
                }
            }
            mock_get.return_value = mock_response

            with self.assertRaises(KeyError) as context:
                get_currencies(['XYZ'])

            error_message = str(context.exception)
            self.assertIn("XYZ", error_message)
            self.assertIn("отсутствует", error_message)

    def test_connection_error(self):
        with patch('main.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

            with self.assertRaises(ConnectionError) as context:
                get_currencies(['USD'])

            self.assertIn("Ошибка подключения", str(context.exception))

    def test_value_error_json(self):
        with patch('main.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = json.JSONDecodeError("Wrong JSON", "", 0)
            mock_get.return_value = mock_response

            with self.assertRaises(ValueError) as context:
                get_currencies(['USD'])

            self.assertIn("Ошибка парсинга JSON", str(context.exception))

    def test_key_missing_valute(self):
        with patch('main.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "Data": {}
            }
            mock_get.return_value = mock_response

            with self.assertRaises(KeyError) as context:
                get_currencies(['USD'])

            self.assertIn("отсутствует ключ 'Valute'", str(context.exception))


class TestLoggerDecorator(unittest.TestCase):
    def test_logging(self):
        stream = io.StringIO()

        @logger(handle=stream)
        def test_function(x):
            return x * 2

        result = test_function(5)
        self.assertEqual(result, 10)

        logs = stream.getvalue()
        self.assertIn("INFO", logs)
        self.assertIn("test_function", logs)
        self.assertIn("Логгер отработал успешно", logs)
        self.assertNotIn("ERROR", logs)

    def test_logging_on_error(self):
        stream = io.StringIO()

        @logger(handle=stream)
        def error_function():
            raise ValueError("Test error message")

        with self.assertRaises(ValueError) as context:
            error_function()

        self.assertIn("Test error message", str(context.exception))

        logs = stream.getvalue()
        self.assertRegex(logs, "ERROR")
        self.assertIn("ValueError", logs)
        self.assertIn("Test error message", logs)

    def test_logger_different_values(self):
        stream = io.StringIO()

        @logger(handle=stream)
        def return_none():
            return None

        @logger(handle=stream)
        def return_list():
            return [1, 2, 3]

        self.assertIsNone(return_none())
        self.assertEqual(return_list(), [1, 2, 3])

        logs = stream.getvalue()
        self.assertIn("return_none", logs)
        self.assertIn("return_list", logs)


class TestStreamWrite(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def wrapped():
            return get_currencies(['USD'], url="https://wrong")

        self.wrapped = wrapped

    def test_logging_error(self):
        with self.assertRaises(ConnectionError):
            self.wrapped()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)
