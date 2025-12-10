import math
import time
from integrate_1 import integrate
from integrate_2_async import integrate_async
from integrate_3_process import integrate_process

try:
    from integrate_cython import integrate_cython

    n_iter = 1_000_000

    print(f"\nТест: интеграл sin(x) от 0 до пи")
    print(f"Количество итераций: {n_iter:,}")
    print("-" * 40)
    # обычный подсчет интеграла без потоков и процессов
    start = time.perf_counter()
    result_integrate_1 = integrate(math.sin, 0, math.pi, n_iter=n_iter)
    time_integrate_1 = time.perf_counter() - start

    # подсчет интеграла с помощью потоков
    start = time.perf_counter()
    result_integrate_2_async = integrate(math.sin, 0, math.pi, n_iter=n_iter)
    time_integrate_2_async = time.perf_counter() - start

    # подсчет интеграла с помощью процессов
    start = time.perf_counter()
    result_integrate_3_process = integrate(math.sin, 0, math.pi, n_iter=n_iter)
    time_integrate_3_process = time.perf_counter() - start

    # Cython
    start = time.perf_counter()
    result_cy = integrate_cython(math.sin, 0, math.pi, n_iter)
    time_cy = time.perf_counter() - start

    # Результаты
    print(f"Integrate_1:  {time_integrate_1:.4f} сек, результат: {result_integrate_1:.5f}")
    print(f"Integrate_2_async:  {time_integrate_2_async:.4f} сек, результат: {result_integrate_2_async:.5f}")
    print(f"Integrate_3_process:  {time_integrate_3_process:.4f} сек, результат: {result_integrate_3_process:.5f}")
    print(f"Cython:  {time_cy:.4f} сек, результат: {result_cy:.5f}")
    # print(f"Ускорение: {time_py / time_cy:.1f}x")
    # print(f"Погрешность Python: {abs(result_py - 2.0):.2e}")
    # print(f"Погрешность Cython: {abs(result_cy - 2.0):.2e}")

except ImportError as e:
    print(f"✗ Ошибка импорта: {e}")
    print("\nСначала скомпилируйте модуль командой:")
    print("python setup.py build_ext --inplace")
    print("\nПроверьте, что в папке есть файлы:")
    print("- integrate_cython.pyx (исходник)")
    print("- integrate_cython.pyd (скомпилированный модуль для Windows)")
    print("- или integrate_cython.so (для Linux/Mac)")