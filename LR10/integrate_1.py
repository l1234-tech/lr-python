import math

def integrate(f, a, b, *, n_iter=1000):
  """
    Вычисляет определенный интеграл функции f на отрезке [a, b] методом левых прямоугольников.

    Parameters:
    f (callable): Функция, интеграл которой вычисляется.
    a (float): Нижний предел интегрирования.
    b (float): Верхний предел интегрирования.
    n_iter (int): Количество итераций (подинтервалов). По умолчанию 1000.

    Returns:
    float: Приближенное значение определенного интеграла.

    Пример реализации:
    >>> round(integrate(math.cos, 0, math.pi / 2, n_iter=100), 5)
    1.00783
  """
  acc = 0
  step = (b - a) / n_iter
  for i in range(n_iter):
    acc += f(a + i*step) * step
  return acc