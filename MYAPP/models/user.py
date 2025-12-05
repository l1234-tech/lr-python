class User:
    def __init__(self, user_id: int, name: str = 'Andrew'):
        self.__id = user_id
        self.__name = name
        self.__subscriptions = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if len(name) >= 1:
            self.__name = name
        else:
            raise ValueError('Имя не может быть меньше одного символа')

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, user_id):
        if user_id > 0 and isinstance(user_id, int):
            self.__id = user_id
        else:
            raise ValueError('ID должно быть положительным числом')

    @property
    def subscriptions(self):
        return self.__subscriptions.copy()

    def add_subscription(self, currency_code: str):
        if currency_code not in self.__subscriptions:
            self.__subscriptions.append(currency_code)
            return True
        return False

    def remove_subscription(self, currency_code: str):
        if currency_code in self.__subscriptions:
            self.__subscriptions.remove(currency_code)
            return True
        return False

    def has_subscription(self, currency_code: str):
        return currency_code in self.__subscriptions

    def get_subscriptions_count(self):
        """Получить количество подписок"""
        return len(self.__subscriptions)

    def to_dict(self):
        """Преобразовать объект в словарь для JSON"""
        return {
            'id': self.__id,
            'name': self.__name,
            'subscriptions': self.__subscriptions.copy(),
            'subscriptions_count': len(self.__subscriptions)
        }

    def __repr__(self):
        return f"User(id={self.__id}, name='{self.__name}', subscriptions={self.__subscriptions})"
