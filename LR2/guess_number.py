def binary_searh(target:int , list_sorted:list, cnt:int):
    """target -> int , list_sorted -> list , cnt -> int
    target - число, которое программа должна угадать
    list_sorted - отсортированный список, среди которого программа должна найти загаданное число
    cnt - число итераций"""
    left , right = 0 , len(list_sorted) - 1
    """left - левая (нижняя) граница списка , right - правая (верхняя) граница списка"""
    while left <= right :
        mid = (left + right ) // 2
        """mid - серединный барьер, с которым мы сравниваем target"""
        cnt += 1
        """для каждого mid мы совершаем 1 итерацию поиска (попытка)"""
        if list_sorted[mid] == target:
            return [target, cnt]
        elif list_sorted[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return [None , cnt]