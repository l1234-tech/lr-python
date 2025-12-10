import concurrent.futures as ftres
from functools import partial
import math

def integrate(f, a, b, *, n_iter=1000):
  acc = 0
  step = (b - a) / n_iter
  for i in range(n_iter):
    acc += f(a + i*step) * step
  return acc

def integrate_async(f, a, b, *, n_jobs=2, n_iter=1000):
    """
    Вычисляет определенный интеграл функции f на отрезке [a, b]
    с использованием ThreadPoolExecutor (потоков).

    Parameters
    ----------
    f : Callable - функция, интеграл которой вычисляется.
    a : float - нижний предел интегрирования.
    b : float - верхний предел интегрирования.
    n_jobs : int - количество потоков для параллельного выполнения.
    n_iter : int, optional - общее количество итераций.
    Returns
    -------
    float - приближенное значение определенного интеграла.

    Пример реализации:
    >>> round(integrate_async(math.log2, 1, 2, n_iter=10000), 5)
    Работник 0, границы: 1.0, 1.5
    Работник 1, границы: 1.5, 2.0
    0.55725
  """
    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)

    spawn = partial(executor.submit, integrate, f, n_iter = n_iter // n_jobs)

    step = (b - a) / n_jobs
    for i in range(n_jobs):
      print(f"Работник {i}, границы: {a + i * step}, {a + (i + 1) * step}")

    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]

    return sum(list(f.result() for f in ftres.as_completed(fs)))