from guess_number import binary_searh
chislo = int(input('Введите угадываемое число = '))
d1 = int(input('Введите нижний порог интервала, в котором находится ваше число = '))
d2 = int(input('Введите верхний порог интервала, в котором находится ваше число = '))
list = list(range(d1, d2 + 1))
print(binary_searh(chislo, list, 0))
