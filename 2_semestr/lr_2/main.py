import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# 1. СОЗДАНИЕ И ОБРАБОТКА МАССИВОВ
# ============================================================

def create_vector():
    """
    Создать одномерный массив целых чисел от 0 до 9 включительно.

    Returns:
        numpy.ndarray: Массив чисел от 0 до 9 включительно.

    Examples
    --------
    >>> v = create_vector()
    >>> v.shape
    (10,)
    >>> v[0], v[-1]
    (0, 9)
    """

    return np.arange(10)

def create_matrix():
    """
    Создать матрицу 5×5 со случайными числами из равномерного распределения [0, 1).

    Returns:
        numpy.ndarray: Матрица 5x5 со случайными значениями от 0 до 1
    """
    return np.random.rand(5,5)

def reshape_vector(vec):
    """
     Изменить форму одномерного массива из (10,) в двумерный (2, 5).

    Args:
        vec (numpy.ndarray): Входной массив формы (10,)

    Returns:
        numpy.ndarray: Преобразованный массив формы (2, 5)

    Raises
    ------
    ValueError
        Если входной массив не может быть преобразован в форму (2, 5).

    Examples
    --------
    >>> v = np.arange(10)
    >>> reshape_vector(v).shape
    (2, 5)
    """
    return vec.reshape(2,5)

def transpose_matrix(mat):
    """
    Выполнить транспонирование матрицы (замена строк на столбцы).

    Args:
        mat (numpy.ndarray): Входная матрица

    Returns:
        numpy.ndarray: Транспонированная матрица

    Examples
    --------
    >>> m = np.array([[1, 2], [3, 4]])
    >>> transpose_matrix(m)
    array([[1, 3],
           [2, 4]])
    """
    return mat.T

# ============================================================
# 2. ВЕКТОРНЫЕ ОПЕРАЦИИ
# ============================================================

def vector_add(a, b):
    """
    Выполнить поэлементное сложение двух векторов одинаковой длины.

    Args:
        a (numpy.ndarray): Первый вектор
        b (numpy.ndarray): Второй вектор

    Returns:
        numpy.ndarray: Результат поэлементного сложения

    Raises
    ------
    ValueError
        Если формы массивов a и b не совпадают.

    Examples
    --------
    >>> vector_add(np.array([1, 2]), np.array([3, 4]))
    array([4, 6])
    """
    return a + b

def scalar_multiply(vec, scalar):
    """
    Умножить вектор на скалярное значение.

    Args:
        vec (numpy.ndarray): Входной вектор
        scalar (float/int): Число для умножения

    Returns:
        numpy.ndarray: Результат умножения вектора на скаляр

    Examples
    --------
    >>> scalar_multiply(np.array([1, 2, 3]), 2)
    array([2, 4, 6])
    """

    return vec * scalar

def elementwise_multiply(a, b):
    """
    Выполнить поэлементное умножение двух массивов.

    Args:
        a (numpy.ndarray): Первый вектор/матрица
        b (numpy.ndarray): Второй вектор/матрица

    Returns:
        numpy.ndarray: Результат поэлементного умножения
    """
    return a * b

def dot_product(a, b):
    """
    Вычислить скалярное произведение двух векторов.

    Args:
        a (numpy.ndarray): Первый вектор
        b (numpy.ndarray): Второй вектор

    Returns:
        float: Скалярное произведение векторов

    Examples
    --------
    >>> dot_product(np.array([1, 2, 3]), np.array([4, 5, 6]))
    32
    """
    return np.dot(a, b)

# ============================================================
# 3. МАТРИЧНЫЕ ОПЕРАЦИИ
# ============================================================

def matrix_multiply(a, b):
    """
    Выполнить матричное умножение двух массивов.

    Args:
        a (numpy.ndarray): Первая матрица
        b (numpy.ndarray): Вторая матрица

    Returns:
        numpy.ndarray: Результат умножения матриц

    Raises
    ------
    ValueError
        Если количество столбцов a не равно количеству строк b.

    Examples
    --------
    >>> A = np.array([[1, 2], [3, 4]])
    >>> B = np.array([[2, 0], [1, 2]])
    >>> matrix_multiply(A, B)
    array([[ 4,  4],
           [10,  8]])
    """
    return a @ b

def matrix_determinant(a):
    """
    Вычислить определитель (детерминант) квадратной матрицы (вычисляется только для квадратной матрицы).

    Args:
        a (numpy.ndarray): Квадратная матрица

    Returns:
        float: Определитель матрицы

    Raises
    ------
    np.linalg.LinAlgError
        Если матрица не является квадратной.

    Examples
    --------
    >>> A = np.array([[1, 2], [3, 4]])
    >>> round(matrix_determinant(A), 5)
    -2.0
    """
    return np.linalg.det(a)

def matrix_inverse(a):
    """
    Вычислить обратную матрицу для квадратной матрицы.

    Args:
        a (numpy.ndarray): Квадратная матрица

    Returns:
        numpy.ndarray: Обратная матрица

    Raises
    ------
    np.linalg.LinAlgError
        Если матрица вырождена (определитель равен нулю) или не квадратная.
    """
    return np.linalg.inv(a)

def solve_linear_system(a, b):
    """
    Решить систему линейных уравнений Ax = b методом наименьших квадратов.

    Args:
        a (numpy.ndarray): Матрица коэффициентов A
        b (numpy.ndarray): Вектор свободных членов b

    Returns:
        numpy.ndarray: Решение системы x

    Raises
    ------
    np.linalg.LinAlgError
        Если система не имеет решения или матрица `a` вырождена.

    Examples
    --------
    >>> A = np.array([[2, 1], [1, 3]])
    >>> b = np.array([1, 2])
    >>> x = solve_linear_system(A, b)
    >>> np.allclose(A @ x, b)
    True
    """
    return np.linalg.solve(a, b)

# ============================================================
# 4. СТАТИСТИЧЕСКИЙ АНАЛИЗ
# ============================================================

def load_dataset(path="data/students_scores.csv"):
    """
    Загрузить данные из CSV-файла и преобразовать в NumPy-массив.

    Args:
        path (str): Путь к CSV файлу

    Returns:
        numpy.ndarray: Загруженные данные в виде массива

    Raises
    ------
    FileNotFoundError
        Если файл по указанному пути не найден.
    pd.errors.EmptyDataError
        Если файл пуст или не содержит данных.

    Examples
    --------
    >>> data = load_dataset('data/sample.csv')
    >>> data.shape
    (10, 3)
    """
    return pd.read_csv(path).to_numpy()

def statistical_analysis(data):
    """
    Выполнить базовый статистический анализ одномерного массива данных.

    Вычисляет следующие метрики:
    - среднее значение (mean);
    - медиана (median);
    - стандартное отклонение (std);
    - минимум и максимум;
    - 25-й и 75-й перцентили.

    Args:
        data (numpy.ndarray): Одномерный массив данных

    Returns:
        dict: Словарь со статистическими показателями

    --------
    numpy.mean : Среднее арифметическое.
    numpy.median : Медиана.
    numpy.std : Стандартное отклонение.
    numpy.percentile : Перцентили распределения.

    Examples
    --------
    >>> data = np.array([10, 20, 30, 40, 50])
    >>> stats = statistical_analysis(data)
    >>> stats['mean']
    30.0
    """
    return {
        "mean": np.mean(data),           
        "median": np.median(data),       
        "std": np.std(data),             
        "min": np.min(data),             
        "max": np.max(data),             
        "25%": np.percentile(data, 25),  
        "75%": np.percentile(data, 75)   
    }

def normalize_data(data: np.ndarray) -> np.ndarray:
    """
    Выполнить Min-Max нормализацию данных к диапазону [0, 1].

    Формула нормализации:
        x_norm = (x - min) / (max - min)

    Args:
        data (numpy.ndarray): Входной массив данных

    Returns:
        numpy.ndarray: Нормализованный массив данных в диапазоне [0, 1]

    Raises
    ------
    ValueError
        Если max == min (все элементы одинаковы).

    Examples
    --------
    >>> data = np.array([0, 5, 10])
    >>> normalize_data(data)
    array([0. , 0.5, 1. ])
    """
    min_val = np.min(data)
    max_val = np.max(data)

    return (data - min_val) / (max_val - min_val)


# ============================================================
# 5. ВИЗУАЛИЗАЦИЯ
# ============================================================

def plot_histogram(data):
    """
    Построить и сохранить гистограмму распределения данных.

    Args:
    ----------
    data : np.ndarray
        Одномерный массив данных для визуализации.
    bins : int, optional
        Количество интервалов гистограммы (по умолчанию 10).
    output_path : str, optional
        Путь для сохранения изображения (по умолчанию "plots/histogram.png").

    Returns
    -------
    None
    """
    plt.hist(data, bins=10, edgecolor='black', alpha=0.7)
    plt.title('Распределение оценок по математике')
    plt.xlabel('Оценка')
    plt.ylabel('Количество студентов')
    plt.savefig('plots/histogram.png', dpi=300, bbox_inches='tight')

def plot_heatmap(matrix):
    """
    Построить и сохранить тепловую карту (heatmap) матрицы данных.

    Args:
    ----------
    matrix : np.ndarray
        Двумерная матрица для визуализации (например, корреляционная).
    output_path : str, optional
        Путь для сохранения изображения (по умолчанию "plots/heatmap.png").

    Returns
    -------
    None
    """
    
    plt.figure(figsize=(10, 8))
    
    sns.heatmap(
        matrix,
        annot=True,           
        fmt='.2f',            
        cmap='coolwarm',      
        center=0,             
        square=False,          
        linewidths=0.5,       
        cbar_kws={'label': 'Корреляция'}  
    )
    
    plt.title('Распределение баллов', fontsize=16, pad=20)
    plt.xlabel('Предмет')
    plt.ylabel('Оценка')
    
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.savefig('plots/heatmap.png', dpi=300, bbox_inches='tight')

def plot_line(x, y):
    """
    Построить и сохранить линейный график зависимости y от x.

    Args:
    ----------
    x : np.ndarray
        Массив значений по оси X (независимая переменная).
    y : np.ndarray
        Массив значений по оси Y (зависимая переменная).
    output_path : str, optional
        Путь для сохранения изображения (по умолчанию "plots/line_plot.png").

    Returns
    -------
    None

    Raises
    ------
    ValueError
        Если длины массивов x и y не совпадают.

    Examples
    --------
    >>> x = np.arange(1, 11)
    >>> y = np.random.randint(60, 100, size=10)
    >>> plot_line(x, y)
    """
    plt.figure(figsize=(12, 6))
    plt.plot(
        x, y,
        marker='o',              # Точки на графике
        linestyle='-',           # Сплошная линия
        linewidth=2,             # Толщина линии
        markersize=6,            # Размер маркеров
        markeredgewidth=1.5,        # Толщина края
        label='Оценка по математике'
    )
    plt.title('Зависимость оценки по математике от номера студента', fontsize=16, pad=20)
    plt.xlabel('Номер студента', fontsize=12)
    plt.ylabel('Оценка', fontsize=12)
    plt.savefig('plots/line_plot.png', dpi=300, bbox_inches='tight')