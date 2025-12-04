class Author:
    def __init__(self, name: str, group: str = "P3122"):
        self.__name = name
        self.__group = group

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
    def group(self):
        return self.__group

    @group.setter
    def group(self, group):
        if len(group) == 5 and isinstance(group, str):
            self.__group = group
        else:
            raise ValueError('Группа должна быть 5 символов длиной')

    def to_dict(self):
        """Преобразовать объект в словарь для JSON"""
        return {
            'name': self.__name,
            'group': self.__group
        }
