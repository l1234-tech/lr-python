class User():
    def __init__(self,id:int, name:str = 'Andrew'):
        self.__id = id
        self.__name = name

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
    def id(self, id):
        if len(id) > 0 and type(id) is int:
            self.id = id
        else:
            raise ValueError('ID должно быть положительным числом')
