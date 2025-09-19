from lr1 import two_sum
import unittest
class TestMySolution(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(two_sum([2,7,11,15] , 9) , [0,1])
        self.assertEqual(two_sum([3, 2], 6), 'Нет решений')
        self.assertEqual(two_sum([3,3,3,3], 6), [0, 1])
        self.assertEqual(two_sum([1,2,3,4,5,6,7,8], 8), [0, 6])
        self.assertEqual(two_sum(['5', 3,3], 6), 'Неверный тип данных')
        self.assertEqual(two_sum([3.1, 3], 6), 'Неверный тип данных')
        self.assertEqual(two_sum([-3, -3], 6), 'Нет решений')
        self.assertEqual(two_sum([3], 6), 'Нет решений')
if __name__ == '__main__':
    unittest.main()
