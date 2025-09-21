from guess_number import binary_searh
import unittest
class TestMySolution(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(binary_searh(2, list(range(1,100)), 0), [2,7])
        # угадывание числа 2 из диапозона 1 - 100

        self.assertEqual(binary_searh(2, list(range(0,50)), 0), [2,4])
        # угадывание числа 2 из диапозона 0 - 50

        self.assertEqual(binary_searh(2, list(range(1, 10000)), 0), [2, 12])
        # угадывание числа 2 из диапозона 1 - 10000

        self.assertEqual(binary_searh(-67, list(range(-100, -50)), 0), [-67, 4])
        # угадывание числа -67 из диапозона -100 - (-50)

        self.assertEqual(binary_searh(2, list(range(-10, 10)), 0), [2, 4])
        # угадывание числа 2 из диапозона -10 - 10

        self.assertEqual(binary_searh(2, list(range(3, 100)), 0), [None, 6])
        # угадывание числа 2 из диапозона 3 - 100 (угадываемое число находится вне интервала)

        self.assertEqual(binary_searh(1234, list(range(123, 1234567)), 0), [1234, 19])
        # угадывание числа 1234 из диапозона 123 - 1234567
if __name__ == '__main__':
    unittest.main()
