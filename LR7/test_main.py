import io
import unittest
import requests
from main import trace
from main import get_currencies
MAX_R_VALUE = 1000

class TestGetCurrencies(unittest.TestCase):


    def test_currency_usd(self):
      currency_list = ['USD']
      currency_data = get_currencies(currency_list)

      self.assertIn(currency_list[0], currency_data)
      self.assertIsInstance(currency_data['USD'], float)
      self.assertGreaterEqual(currency_data['USD'], 0)
      self.assertLessEqual(currency_data['USD'], MAX_R_VALUE)

    def test_nonexist_code(self):
      self.assertIn("Код валюты", get_currencies(["XYZ"])["XYZ"])
      self.assertIn("XYZ", get_currencies(["XYZ"])["XYZ"])
      self.assertIn("не найден", get_currencies(["XYZ"])["XYZ"])

    def test_get_currency_error(self):
        error_phrase_regex = "Ошибка при запросе к API"
        currency_list = ['USD']
        with self.assertRaises(requests.exceptions.RequestException):
            currency_data = get_currencies(currency_list, url="https://")

class TestStreamWrite(unittest.TestCase):


  def setUp(self):
    self.nonstandardstream = io.StringIO()
    self.trace = trace(get_currencies, handle=self.nonstandardstream)

  def test_broken_trace(self):
      broken_stream = io.StringIO()
      broken_stream.write('error_phrase_regex')
      # создали заведомо сломанный поток, который заменяет изначальный, т.е. если в main был бы некорректный поток, то на тесте
      # эта функция перехватила бы этот поток и запутила тест, который выдал бы исключение
      with self.assertRaises(requests.exceptions.RequestException):
          get_currencies(['USD'] , url = "https://", handle = broken_stream)
      #     здесь мы проверяем неверный поток
      broken_regex = broken_stream.getvalue()
      # здесь получаем то, что содержит в себе сломанный поток
      self.assertRegex(broken_regex, "Ошибка при запросе API")

  def test_writing_stream(self):
    with self.assertRaises(requests.exceptions.RequestException):
        self.trace(['USD'], url="https://")


  def tearDown(self):
    del self.nonstandardstream


if __name__ == '__main__':
    unittest.main()

