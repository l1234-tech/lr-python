from pprint import pprint

def gen_bin_tree(height:int , root:int) -> list:
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


    """
    def left_leaf(root):
        return (root - 8) * 3

    def right_leaf(root):
        return (root + 8) * 2
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
                def build_subtree(index: int, level: int, max_level: int) -> tuple:
                    """
                    Функция по характеристикам списка (tree) преобразует его в словарь

                    index - текущая позиция в списке
                    level - текущий уровень в дереве
                    max_level - максимальная высота дерева

                    """
                    if level > max_level:
                        return {}, index
                    # случай, когда уровень превышает макс. высоту, возвращаем пустой словарь

                    node = tree[index]
                    index += 1

                    if level == max_level:
                        return {node}, index
                    # достигнут макс. высота дерева, возвращает дерево

                    left_child, index = build_subtree(index, level + 1, max_level)
                    right_child, index = build_subtree(index, level + 1, max_level)

                    return {node: [left_child, right_child]}, index

                if not tree:
                    return {}

                else:

                    n = len(tree)
                    height = 0
                    while (2 ** (height + 1) - 1) < n:
                        height += 1
                    # вычисление высоты дерева

                    result, _ = build_subtree(0, 0, height)
                    return result

            return to_dict(tree)

pprint((gen_bin_tree(5,18)))