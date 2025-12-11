import cython

# ==================== ВЕРСИЯ 1: ОБЩАЯ (для любых Python функций) ====================
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def integrate_cython(f, double a, double b, int n_iter=1000):
    """
    Универсальная версия для любых Python функций.
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x

    for i in range(n_iter):
        x = a + i * step
        acc += f(x) * step

    return acc


# ==================== ВЕРСИЯ 2: СПЕЦИАЛИЗИРОВАННЫЕ (максимальная скорость) ====================

# Импортируем C-функции напрямую
from libc.math cimport sin, cos, exp, sqrt

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef double integrate_sin(double a, double b, int n_iter=1000):
    """Специальная версия для sin(x). Максимально быстрая."""
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x

    for i in range(n_iter):
        x = a + i * step
        acc += sin(x) * step

    return acc


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef double integrate_cos(double a, double b, int n_iter=1000):
    """Специальная версия для cos(x)."""
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x

    for i in range(n_iter):
        x = a + i * step
        acc += cos(x) * step

    return acc


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef double integrate_exp(double a, double b, int n_iter=1000):
    """Специальная версия для exp(x)."""
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x

    for i in range(n_iter):
        x = a + i * step
        acc += exp(x) * step

    return acc


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef double integrate_pow2(double a, double b, int n_iter=1000):
    """Специальная версия для x²."""
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x

    for i in range(n_iter):
        x = a + i * step
        acc += (x * x) * step

    return acc


# ==================== ВЕРСИЯ 3: ДЛЯ НЕСКОЛЬКИХ ФУНКЦИЙ ====================

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef double integrate_math_func(str func_name, double a, double b, int n_iter=1000):
    """
    Универсальная версия для встроенных математических функций.
    Принимает имя функции как строку.
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x

    if func_name == "sin":
        for i in range(n_iter):
            x = a + i * step
            acc += sin(x) * step
    elif func_name == "cos":
        for i in range(n_iter):
            x = a + i * step
            acc += cos(x) * step
    elif func_name == "exp":
        for i in range(n_iter):
            x = a + i * step
            acc += exp(x) * step
    elif func_name == "sqrt":
        for i in range(n_iter):
            x = a + i * step
            if x >= 0:
                acc += sqrt(x) * step
    elif func_name == "pow2":
        for i in range(n_iter):
            x = a + i * step
            acc += (x * x) * step
    else:
        # Для неизвестных функций возвращаем 0
        return 0.0

    return acc