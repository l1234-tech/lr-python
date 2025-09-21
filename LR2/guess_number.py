def binary_search(target:int , list_sorted:list, cnt:int):
    """
    target -> int , list_sorted -> list , cnt -> int

    target - число, которое программа должна угадать

    list_sorted - отсортированный список, среди которого программа должна найти загаданное число

    cnt - число итераций (попытки, которые программа потратила, чтобы отгадать число)

    left - левая (нижняя) граница списка , right - правая (верхняя) граница списка

    Testing binary_search:

    Made some test for binary_search:
    >> binary_search(2 , [0 , 50] , 0)
    [2 , 4]
    >> binary_search(1,[1,64],0)
    [1,6]
    >> binary_search(2,[-10,10],0)
    [2,4]
    """
    left , right = 0 , len(list_sorted) - 1
    while left <= right :
        mid = (left + right ) // 2
        cnt += 1
        if list_sorted[mid] == target:
            return [target, cnt]
        elif list_sorted[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return [None , cnt]
