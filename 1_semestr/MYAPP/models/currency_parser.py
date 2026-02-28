import requests
from datetime import datetime, timedelta
import json
import time


class CurrencyParser:
    def __init__(self, api_url: str = 'https://www.cbr-xml-daily.ru/daily_json.js'):
        self.api_url = api_url
        self._currencies_data = {}
        self._available_currencies_cache = None
        self._last_update_time = 0
        self._cache_duration = 300

    def get_all_available_currencies(self):
        """Получает список всех доступных валют"""
        current_time = time.time()
        if (self._available_currencies_cache is not None and
                current_time - self._last_update_time < self._cache_duration):
            return self._available_currencies_cache

        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "Valute" in data:
                currencies = list(data["Valute"].keys())
                currencies.append('RUB')
                self._available_currencies_cache = currencies
                self._last_update_time = current_time
                return currencies
            return ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'RUB']

        except Exception as e:
            print(f"Ошибка при запросе API для списка валют: {e}")
            return ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CHF', 'CAD', 'AUD', 'RUB']

    def get_currency_history(self, currency_code: str, days: int = 30):
        """Получает историю курса валюты за последние дни"""
        try:
            if currency_code == 'RUB':
                history = []
                for i in range(days):
                    date_str = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                    history.append({
                        "date": date_str,
                        "value": 1.0
                    })
                return history

            history = []
            current_date = datetime.now()
            successful_days = 0

            for i in range(days):
                if successful_days >= 30:
                    break

                date_str = (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
                url = f"https://www.cbr-xml-daily.ru/archive/{date_str.replace('-', '/')}/daily_json.js"

                try:
                    response = requests.get(url, timeout=3)
                    if response.status_code == 200:
                        data = response.json()
                        if "Valute" in data and currency_code in data["Valute"]:
                            history.append({
                                "date": date_str,
                                "value": data["Valute"][currency_code]["Value"]
                            })
                            successful_days += 1
                except Exception:
                    continue

            if len(history) < 7:
                print(f"Мало данных для {currency_code}, создаем фиктивные данные")
                history = self._generate_mock_history(currency_code, days)

            return history
        except Exception as e:
            print(f"Ошибка при получении истории для {currency_code}: {e}")
            return self._generate_mock_history(currency_code, days)

    def _generate_mock_history(self, currency_code: str, days: int):
        """Генерирует фиктивные данные для истории, если реальные данные недоступны"""
        history = []
        current_date = datetime.now()

        base_values = {
            'USD': 90.0, 'EUR': 98.0, 'GBP': 115.0, 'JPY': 0.6,
            'CNY': 12.5, 'CHF': 105.0, 'CAD': 65.0, 'AUD': 60.0,
            'KZT': 0.19, 'UAH': 2.3, 'BYN': 28.0, 'AMD': 0.23
        }

        base_value = base_values.get(currency_code, 50.0)

        import random
        for i in range(days):
            date_str = (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
            variation = base_value * 0.02 * (random.random() - 0.5)
            history.append({
                "date": date_str,
                "value": base_value + variation
            })

        return history

    def get_currencies(self, currency_codes: list):
        """Получает данные для списка валют"""
        from .currency import CurenciesList

        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()

            currencies = {}
            not_found = []

            if "Valute" in data:
                for code in currency_codes:
                    if code == 'RUB':
                        currency = CurenciesList(
                            name_curr='RUB',
                            currency_id='R00001',
                            name='Российский рубль',
                            value=1.0,
                            previous=1.0
                        )
                        currencies['RUB'] = currency
                    elif code in data["Valute"]:
                        currency_info = data["Valute"][code]
                        currency = CurenciesList(
                            name_curr=code,
                            currency_id=currency_info["ID"],
                            name=currency_info["Name"],
                            value=currency_info["Value"],
                            previous=currency_info["Previous"]
                        )
                        currencies[code] = currency
                    else:
                        not_found.append(code)

            for code in not_found:
                print(f"Валюта {code} не найдена в API, создаем фиктивные данные")
                currency = self._create_mock_currency(code)
                if currency:
                    currencies[code] = currency

            self._currencies_data.update(currencies)
            return currencies

        except Exception as e:
            print(f"Ошибка при запросе API для курсов: {e}")
            currencies = {}
            for code in currency_codes:
                currency = self._create_mock_currency(code)
                if currency:
                    currencies[code] = currency
            return currencies

    def _create_mock_currency(self, currency_code: str):
        """Создает фиктивную валюту если она не найдена в API"""
        from .currency import CurenciesList

        mock_data = {
            'USD': ('Доллар США', 90.5, 89.8),
            'EUR': ('Евро', 98.2, 97.5),
            'GBP': ('Фунт стерлингов', 115.3, 114.7),
            'JPY': ('Японская иена', 0.61, 0.60),
            'CNY': ('Китайский юань', 12.6, 12.4),
            'CHF': ('Швейцарский франк', 105.1, 104.8),
            'CAD': ('Канадский доллар', 65.2, 64.9),
            'AUD': ('Австралийский доллар', 60.1, 59.8),
            'KZT': ('Казахстанский тенге', 0.19, 0.188),
            'UAH': ('Украинская гривна', 2.3, 2.28),
            'BYN': ('Белорусский рубль', 28.0, 27.8),
            'AMD': ('Армянский драм', 0.23, 0.228),
            'RUB': ('Российский рубль', 1.0, 1.0),
        }

        if currency_code in mock_data:
            name, value, previous = mock_data[currency_code]
            return CurenciesList(
                name_curr=currency_code,
                currency_id=f'MOCK{currency_code}',
                name=name,
                value=value,
                previous=previous
            )
        else:
            return CurenciesList(
                name_curr=currency_code,
                currency_id=f'UNKNOWN{currency_code}',
                name=f'Валюта {currency_code}',
                value=50.0,
                previous=49.5
            )

    def get_currency_info(self, currency_code: str):
        """Получает информацию о конкретной валюте"""
        currencies = self.get_currencies([currency_code])

        return currencies.get(currency_code)
