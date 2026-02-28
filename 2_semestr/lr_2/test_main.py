import unittest
import os
import numpy as np
from main import plot_heatmap, plot_histogram, statistical_analysis, load_dataset, solve_linear_system, matrix_inverse, matrix_determinant, matrix_multiply, create_vector, create_matrix, reshape_vector, transpose_matrix, vector_add, scalar_multiply, elementwise_multiply, dot_product

class Test_numpy_lr2(unittest.TestCase):

# ============================================================
# 1. СОЗДАНИЕ И ОБРАБОТКА МАССИВОВ
# ============================================================

    def test_create_vector(self):
        v = create_vector()
        assert isinstance(v, np.ndarray)
        assert v.shape == (10,)
        assert np.array_equal(v, np.arange(10))

    def test_create_matrix(self):
        m = create_matrix()
        assert isinstance(m, np.ndarray)
        assert m.shape == (5, 5)
        assert np.all((m >= 0) & (m < 1))

    def test_reshape_vector(self):
        v = np.arange(10)
        reshaped = reshape_vector(v)
        assert reshaped.shape == (2, 5)
        assert reshaped[0, 0] == 0
        assert reshaped[1, 4] == 9

    def test_transpose_matrix(self):
        mat = np.random.rand(5,5)
        T_mat = transpose_matrix(mat)
        assert isinstance(T_mat, np.ndarray)
        assert T_mat.shape == (5, 5)
        assert np.all(T_mat[j, i] == mat[i, j] 
            for i in range(mat.shape[0]) 
            for j in range(mat.shape[1]))
        
# ============================================================
# 2. ВЕКТОРНЫЕ ОПЕРАЦИИ
# ============================================================
    
    def test_vector_add(self):
        assert np.array_equal(
            vector_add(np.array([1,2,3]), np.array([4,5,6])),
            np.array([5,7,9])
        )
        assert np.array_equal(
            vector_add(np.array([0,1]), np.array([1,1])),
            np.array([1,2])
        )
    
    def test_scalar_multiply(self):
        assert np.array_equal(
            scalar_multiply(np.array([1,2,3]), 2),
            np.array([2,4,6])
        )

    def test_elementwise_multiply(self):
        assert np.array_equal(
            elementwise_multiply(np.array([1,2,3]), np.array([4,5,6])),
            np.array([4,10,18])
        )
    
    def test_dot_product(self):
        assert dot_product(np.array([1,2,3]), np.array([4,5,6])) == 32
        assert dot_product(np.array([2,0]), np.array([3,5])) == 6


# ============================================================
# 3. МАТРИЧНЫЕ ОПЕРАЦИИ
# ============================================================
    
    def test_matrix_multiply(self):
        A = np.array([[1,2],[3,4]])
        B = np.array([[2,0],[1,2]])
        assert np.array_equal(matrix_multiply(A,B), A @ B)

    def test_matrix_determinant(self):
        A = np.array([[1,2],[3,4]])
        assert round(matrix_determinant(A),5) == -2.0

    
    def test_matrix_inverse(self):
        A = np.array([[1,2],[3,4]])
        invA = matrix_inverse(A)
        assert np.allclose(A @ invA, np.eye(2))
    
    def test_solve_linear_system(self):
        A = np.array([[2,1],[1,3]])
        b = np.array([1,2])
        x = solve_linear_system(A,b)
        assert np.allclose(A @ x, b)

# ============================================================
# 4. СТАТИСТИЧЕСКИЙ АНАЛИЗ
# ============================================================

    def test_load_dataset(self):
        # Для теста создадим временный файл
        test_data = "math,physics,informatics\n78,81,90\n85,89,88"
        with open("test_data.csv", "w") as f:
            f.write(test_data)
        try:
            data = load_dataset("test_data.csv")
            assert data.shape == (2, 3)
            assert np.array_equal(data[0], [78,81,90])
        finally:
            os.remove("test_data.csv")

    def test_statistical_analysis(self):
        data = np.array([10,20,30])
        result = statistical_analysis(data)
        assert result["mean"] == 20
        assert result["min"] == 10
        assert result["max"] == 30

# ============================================================
# 5. ВИЗУАЛИЗАЦИЯ
# ============================================================

    def test_plot_histogram(self):
        data = np.random.normal(loc=75, scale=10, size=100) 
        plot_histogram(data)
        # Проверяем, что файл был создан
        self.assertTrue(os.path.exists('plots/histogram.png'))

    def test_plot_heatmap(self):
        data = np.random.normal(loc=75, scale=10, size=100) 
        plot_heatmap(data)
        # Проверяем, что файл был создан
        self.assertTrue(os.path.exists('plots/heatmap.png'))
    
if __name__ == '__main__':
    unittest.main()