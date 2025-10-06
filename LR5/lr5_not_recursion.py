from pprint import pprint

def gen_bin_tree(height:int , root:int) -> dict:
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

pprint((gen_bin_tree(5,18)))
