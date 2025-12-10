import math
import concurrent.futures as ftres
from functools import partial

def integrate(f, a, b, *, n_iter=1000):
  acc = 0
  step = (b - a) / n_iter
  for i in range(n_iter):
    acc += f(a + i*step) * step
  return acc

def integrate_process(f, a, b, *, n_jobs=2, n_iter=1000):
    """
    Вычисляет определенный интеграл функции f на отрезке [a, b] с использованием ProcessPoolExecutor (процессов).

    Parameters
    ----------
    f : Callable - функция, интеграл которой вычисляется.
    a : float - нижний предел интегрирования.
    b : float - верхний предел интегрирования.
    n_jobs : int - количество процессов для параллельного выполнения.
    n_iter : int - общее количество итераций.

    Returns
    -------
    float - приближенное значение определенного интеграла.

    Пример реализации:
    >>> round(integrate_process(math.sin, 0, math.pi, n_jobs=2, n_iter=1000), 5)
    Распределение работы между 2 процессами:
  Процесс 0: отрезок [0.0000, 1.5708], итераций: 500
  Процесс 1: отрезок [1.5708, 3.1416], итераций: 500
2.0
    """
    executor = ftres.ProcessPoolExecutor(max_workers=n_jobs)

    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)

    step = (b - a) / n_jobs
    print(f"Распределение работы между {n_jobs} процессами:")
    for i in range(n_jobs):
        print(f"  Процесс {i}: отрезок [{a + i * step:.4f}, {a + (i + 1) * step:.4f}], "
              f"итераций: {n_iter // n_jobs}")

    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]

    results = [future.result() for future in ftres.as_completed(fs)]

    return sum(results)