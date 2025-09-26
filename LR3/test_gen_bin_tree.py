from lr3 import gen_bin_tree , left_leaf , right_leaf
import unittest
class TestMySolution(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(gen_bin_tree(0, 18), [18])
        # строим бинарное дерево, где высота 0, то есть должно вывести просто root

if __name__ == '__main__':
    unittest.main()