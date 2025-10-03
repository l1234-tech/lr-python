from pprint import pprint

def gen_bin_tree(height:int , root:int) -> list:
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

    if type(height) in (str, list):
        return "Некорректное значение height (должно быть натуральное число или 0)"

    elif type(root) in (str, list):
        return "Некорректное значение root (должно быть неотрицательное число)"

    else:
        if height < 0 or int(height) != height:
            return "Некорректное значение height (должно быть натуральное число или 0)"

        elif root < 0:
            return "Некорректное значение root (должно быть неотрицательное число)"

        elif height == 0:
            return {root}

        else:
            res = {root:  [gen_bin_tree(height - 1 , left_leaf(root)),  gen_bin_tree(height - 1, right_leaf(root))]}
            return res

pprint(gen_bin_tree(5, 18))
