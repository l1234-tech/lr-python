# models/currency.py
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

    def to_dict(self):
        """Преобразовать объект в словарь для JSON"""
        return {
            'name_curr': self.__name_curr,
            'id': self.__id,
            'price': self.__price,
            'name': self.__full_name,
            'previous': self.__previous
        }