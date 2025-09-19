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

        self.assertEqual(binary_searh(2, list(range(-100, -50)), 0), [2, 6])
        self.assertEqual(binary_searh(2, list(range(1, 100)), 0), [2, 7])
        self.assertEqual(binary_searh(2, list(range(1, 100)), 0), [2, 7])
        self.assertEqual(binary_searh(2, list(range(1, 100)), 0), [2, 7])
if __name__ == '__main__':
    unittest.main()
