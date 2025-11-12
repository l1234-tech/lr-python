import requests

class CurenciesList:
    def __init__(self, name_curr: str, currency_id: str,
                 name: str = "", value: float = 0.0, previous: float = 0.0):
        self.__id = currency_id
        self.__name_curr = name_curr
        self.__price = value
        self.__full_name = name
        self.__previous = previous

    @property
    def name_curr(self):
        return self.__name_curr

    @name_curr.setter
    def name_curr(self, name_curr):
        if len(name_curr) == 3:
            self.__name_curr = name_curr
        else:
            raise ValueError('Имя валюты должно содержать 3 символа')

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, currency_id):
        if currency_id and isinstance(currency_id, str):
            self.__id = currency_id
        else:
            raise ValueError('ID должно быть непустой строкой')

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        if price > 0 and isinstance(price, (float, int)):
            self.__price = float(price)
        else:
            raise ValueError('Цена должна быть положительным числом')

    @property
    def name(self):
        return self.__full_name

    @property
    def previous(self):
        return self.__previous


    def __str__(self):
        return f"{self.name_curr} ({self.id}): {self.price:.4f} руб."

    def __repr__(self):
        return f"Currency('{self.name_curr}', '{self.id}', {self.price})"


class CurrencyParser:
    """
    Этот класс нужен для того, чтобы "парсить" (получать) информацию о валютах из функции get_currencies
    """
    def __init__(self, api_url: str = 'https://www.cbr-xml-daily.ru/daily_json.js'):
        self.api_url = api_url
        self._currencies_data = {}

    def get_all_available_currencies(self):
        """
        Получает список всех доступных валют из API ЦБ, чтобы пользователь мог выбрать любую интересующую валюту
        """
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()

            if "Valute" in data:
                # Возвращаем список всех кодов валют
                return list(data["Valute"].keys())
            else:
                return []

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе API: {e}")
            return []

    def get_currencies(self, currency_codes: list):
        """
        Эта функция получает из api ЦБ все курсы валют
        """
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()

            currencies = {}

            if "Valute" in data:
                for code in currency_codes:
                    if code in data["Valute"]:
                        currency_info = data["Valute"][code]
                        currency = CurenciesList(
                            name_curr=code,
                            currency_id=currency_info["ID"],
                            # это id валюты
                            name=currency_info["Name"],
                            # это имя валюты (пример: Доллар)
                            value=currency_info["Value"],
                            # курс валюты
                            previous=currency_info["Previous"]
                        #     предыдущий курс валюты, чтобы выяснить измененине
                        )
                        currencies[code] = currency

            self._currencies_data.update(currencies)
            return currencies

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе API: {e}")
            return {}

    def update_selected_currencies(self, new_currencies: list):
        """Обновляет список отслеживаемых валют"""
        return self.get_currencies(new_currencies)