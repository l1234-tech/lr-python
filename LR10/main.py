from integrate_1 import integrate
from integrate_2_async import integrate_async
from integrate_3_process import integrate_process
import math

if __name__ == '__main__':
    print(integrate(math.log2, 1, 2))
    print('-' * 10)
    print(round(integrate_async(math.log2, 1, 2, n_iter=10000), 5))
    print('-' * 10)
    print(round(integrate_process(math.sin, 0, math.pi, n_jobs=2, n_iter=1000), 5))
    print('-' * 10)