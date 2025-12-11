from integrate_1 import integrate
from integrate_2_async import integrate_async
from integrate_3_process import integrate_process
from cython_integrate import integrate_cython
from integrate_5_noGIL import worker, integrate_processes_mp
import math
import time

if __name__ == '__main__':
    print(round(integrate(math.log2, 1, 2), 5))
    print('-' * 10)
    print(round(integrate_async(math.log2, 1, 2, n_jobs= 2,n_iter=10000), 5))
    print('-' * 10)
    print(round(integrate_process(math.log2, 1, 2, n_jobs=2, n_iter=10000), 5))
    print('-' * 10)
    print(round(integrate_cython(math.log2, 1, 2, n_iter=10000), 5))
    print('-' * 10)
    try:
        n_iter = 10_000_000

        print(f"\nТест: интеграл sin(x) от 0 до пи")
        print(f"Количество итераций: {n_iter:,}")
        print("-" * 40)
        # обычный подсчет интеграла без потоков и процессов
        start = time.perf_counter()
        result_integrate_1 = integrate(math.sin, 0, math.pi, n_iter=n_iter)
        time_integrate_1 = time.perf_counter() - start

        # подсчет интеграла с помощью потоков
        start = time.perf_counter()
        result_integrate_2_async = integrate_async(math.sin, 0, math.pi, n_iter=n_iter)
        time_integrate_2_async = time.perf_counter() - start

        # подсчет интеграла с помощью процессов
        start = time.perf_counter()
        result_integrate_3_process = integrate_process(math.sin, 0, math.pi, n_iter=n_iter)
        time_integrate_3_process = time.perf_counter() - start

        # Cython
        start = time.perf_counter()
        result_cy = integrate_cython(math.sin, 0, math.pi, n_iter)
        time_cy = time.perf_counter() - start

        # мультипроцессинг (noGIL)
        start = time.perf_counter()
        result_5_processes_mp = integrate_processes_mp(math.sin, 0, math.pi, n_jobs=2,n_iter=n_iter)
        time_5_processes_mp = time.perf_counter() - start

        # Результаты
        print('-' * 10)
        print(f"Integrate_1:  {time_integrate_1:.4f} сек, результат: {result_integrate_1:.5f}")
        print(f"Integrate_2_async:  {time_integrate_2_async:.4f} сек, результат: {result_integrate_2_async:.5f}")
        print(f"Integrate_3_process:  {time_integrate_3_process:.4f} сек, результат: {result_integrate_3_process:.5f}")
        print(f"Cython:  {time_cy:.4f} сек, результат: {result_cy:.5f}")
        print(f"Integrate_5_processes_mp:  {time_5_processes_mp:.4f} сек, результат: {result_5_processes_mp:.5f}")
        print('-' * 10)
        for n_jobs in [2, 4, 6, 8, 10]:
            print(f"\n{n_jobs} процессов (multiprocessing):")
            start = time.perf_counter()
            result = integrate_processes_mp(math.sin, 0, math.pi, n_jobs=n_jobs, n_iter=n_iter)
            elapsed = time.perf_counter() - start
            print(f"  Время: {elapsed:.4f} сек")
            print(f"  Результат: {result:.6f}")
            print('-' * 10)

    except ImportError as e:
        print(f"Ошибка импорта: {e}")
