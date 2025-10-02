from lr3 import gen_bin_tree
import unittest
class TestMySolution(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(gen_bin_tree(0, 18), [18])
        # строим бинарное дерево, где высота 0, то есть должно вывести просто root

        self.assertEqual(gen_bin_tree(-1, 18), "Некорректное значение height (должно быть натуральное число или 0)")
        # строим бинарное дерево, где высота отрицательна

        self.assertEqual(gen_bin_tree(1, 18), [18, 30, 52])
        # строим бинарное дерево, где высота больше нуля

        self.assertEqual(gen_bin_tree(1.1, 18), "Некорректное значение height (должно быть натуральное число или 0)")
        # строим бинарное дерево, где высота нецелое число

        self.assertEqual(gen_bin_tree('Привет', 18), "Некорректное значение height (должно быть натуральное число или 0)")
        # строим бинарное дерево, где высота имеет тип str

        self.assertEqual(gen_bin_tree(1, -10), "Некорректное значение root (должно быть неотрицательное число)")
        # строим бинарное дерево, где root меньше нуля

        self.assertEqual(gen_bin_tree(1, "Привет"), "Некорректное значение root (должно быть неотрицательное число)")
        # строим бинарное дерево, где root имеет тип str

        self.assertEqual(gen_bin_tree(1, [12]), "Некорректное значение root (должно быть неотрицательное число)")
        # строим бинарное дерево, где root имеет тип list

if __name__ == '__main__':
    unittest.main()
