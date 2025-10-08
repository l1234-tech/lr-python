import timeit
import matplotlib.pyplot as plt
import random
from functools import lru_cache

def build_tree_recursive(root: int, height: int) -> dict:
    """
    Данная функция строит "бинарное дерево" по двум вводным: выосте и корню дерева
    Также в данной функции есть две подфункции: left_lean и right_lean

    left_lean - функция, преобразовывающая левую "ветку" дерева по заданной функции
    right_lean - функция, преобразовывающая левую "ветку" дерева по заданной функции

    Функция реализована рекурсионным методом, то есть она сторит последующий ответ по уже высчитанному ответу:

    Example:
    >> gen_bin_tree(0,10):
    {10}

    Далее функция строит вычисления для height = 1 на основе значения gen_bin_tree(1,10):

    >> gen_bin_tree(1,10):
    {10: [{6}, {36}]}

    Arguments:
    height (int) - это высота "бинорного дерева"
    root (int) - это корень "бинарного дерева" , то есть первое число, по которому строится дерево

    Returns:
        list и str , list - вывод "бинарного дерева", когда height >= 0
        str - ошибка ввода высоты

    Testing gen_bin_tree:

    Made some test for gen_bin_tree:
        >> gen_bin_tree(1,11):
        {11: [{9}, {38}]}

        >> gen_bin_tree(3,13):
        {13: [{15: [{21: [{39}, {58}]}, {46: [{114}, {108}]}]},
      {42: [{102: [{282}, {220}]}, {100: [{276}, {216}]}]}]}

        >> gen_bin_tree(2,100):
        {100: [{276: [{804}, {568}]}, {216: [{624}, {448}]}]}

    (pprint библиотека для более красивого и читабельного вывода)
    """

    def left_leaf(root):
        return (root - 8) * 3

    def right_leaf(root):
        return (root + 8) * 2

    if height == 0:
        return {root}

    left_result = build_tree_recursive(left_leaf(root), height - 1)

    right_result = build_tree_recursive(right_leaf(root), height - 1)

    return {root: [left_result, right_result]}

    # except RecursionError:
    #
    #     # Если произошла ошибка рекурсии, возвращаем частичное дерево
    #
    #     return {
    #
    #         root: [
    #
    #             "RecursionError - tree too deep",
    #
    #             "RecursionError - tree too deep"
    #
    #         ]
    #
    #     }


def build_tree_iteractive(root:int , height: int) -> dict:
    """
    Данная функция строит "бинарное дерево" по двум вводным: выосте (height) и корню (root) дерева
    Также в данной функции есть две подфункции: left_lean и right_lean

    left_lean - функция, преобразовывающая левую "ветку" дерева по заданной функции
    right_lean - функция, преобразовывающая левую "ветку" дерева по заданной функции

    Функция реализована нерекурсионно, а через цикл.

    Аргументы:
    height (int) - это высота "бинорного дерева"
    root (int) - это корень "бинарного дерева" , то есть первое число, по которому строится дерево
    tree (list) - это список со всему значениями (root) дерева
    cnt (int) - это текущий уровень (высота) дерева
    flag (int) - это количество root на определенном уровне дерева (т.е. height = 0 -> flag = 1 , height = 2 -> flag = 4)

    также есть подфункция to_dict , которая преобразует type(tree) = list в type(tree) = dict:
    >> [18,30,52] -> {18: [{30}, {52}]}

    Примеры запуска:

    >> gen_bin_tree(2,19)
    {19: [{33: [{54}, {75}]}, {82: [{138}, {124}]}]}

    >> gen_bin_tree(4,19)
    {19: [{33: [{54: [{75: [{82}, {138}]}, {124: [{201}, {166}]}]},
            {222: [{180: [{390}, {292}]}, {348: [{264}, {579}]}]}]},
      {418: [{474: [{348: [{642}, {460}]}, {516: [{376}, {1146}]}]},
             {796: [{852: [{600}, {1020}]}, {712: [{768}, {544}]}]}]}]}

    >> gen_bin_tree(0,19)
    [19]

    (pprint библиотека для более красивого и читабельного вывода)

    """
    def left_leaf(root):
        return (root - 8) * 3
    # преобразует root в каждой левой ветке в 3 * (root - 8)

    def right_leaf(root):
        return (root + 8) * 2
    # преобразует root в каждой правой ветке в 2 * (root + 8)

    if type(height) in (str,list):
        return "Некорректное значение height (должно быть натуральное число или 0)"

    elif type(root) in (str,list):
        return "Некорректное значение root (должно быть неотрицательное число)"

    else:
        if height != int(height) or height < 0:
            return "Некорректное значение height (должно быть натуральное число или 0)"
        elif root < 0:
            return "Некорректное значение root (должно быть неотрицательное число)"
        else:
            tree = []
            tree.append(root)
            cnt = 0
            if height == 0:
                return tree
            if height > 0:
                while cnt < height:
                    cnt += 1
                    flag = 2 ** (cnt - 1)
                    for i in tree[-flag:]:
                        tree.append(left_leaf(i))
                        tree.append(right_leaf(i))


            def to_dict(tree: list) -> dict:
                def build_dict_tree(index: int, level: int, max_level: int) -> tuple:
                    """
                    Функция по характеристикам списка (tree) преобразует его в словарь

                    index - текущая позиция в списке
                    level - текущий уровень в дереве
                    max_level - максимальная высота дерева

                    """
                    if level > max_level:
                        return {}, index
                    # случай, когда уровень превышает макс. высоту, возвращаем пустой словарь

                    leaf = tree[index]
                    index += 1

                    if level == max_level:
                        return {leaf}, index
                    # достигнут макс. высота дерева, возвращает дерево

                    left_brench, index = build_dict_tree(index, level + 1, max_level)
                    right_brench, index = build_dict_tree(index, level + 1, max_level)
                    # повышаем level на 1, тк мы левую ветку спискаем на один, высоту увеличиваем на 1

                    return {leaf: [left_brench, right_brench]}, index
                # leaf - основание ветки, left_brench - левое ответвление ветки, right_brench - правое ответвление ветки

                if not tree:
                    return {}
                # проверка на то, что дерево пустой список

                else:

                    n = len(tree)
                    height = 0
                    while (2 ** (height + 1) - 1) < n:
                        height += 1
                    # вычисление высоты дерева, тк у нас есть в функции только tree с типом list

                    result, _ = build_dict_tree(0, 0, height)
                    # индекс в начале 0, также как и уровень, тк мы начинаем строить наше дерево в данной функции с вершины (сверху)
                    return result
            #     здесь result, _ - это нижнее подчеркивание нужно, чтобы реузльтат был не tuple, а dict

            return to_dict(tree)

def benchmark(func, height, root, number=1, repeat=5):
    """Возвращает среднее время выполнения func на наборе data"""
    total = 0
    for n in range(height):
        times = timeit.repeat(lambda: func(root, height), number=number, repeat=repeat)
        total += min(times)  # берём минимальное время из серии
    return total / height


def main():
    # фиксированный набор данных
    random.seed(42)
    test_data = list(range(1, 7, 1))

    res_recursive = []
    res_iterative = []
    root = 18

    for height in test_data:
        res_recursive.append(benchmark(build_tree_recursive, height , root, number=1000, repeat=10))
        res_iterative.append(benchmark(build_tree_iteractive, height , root, number=1000, repeat=10))

    # Визуализация
    plt.plot(test_data, res_recursive, label="Рекурсивный")
    plt.plot(test_data, res_iterative, label="Итеративный")
    plt.xlabel("height")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного 'бинарного дерева'")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
