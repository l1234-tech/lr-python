def two_sum(nums , target):
  for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
      if nums[i] == str(nums[i]) or nums[j] == str(nums[j]) or target == str(target):
        return 'Неверный тип данных'
        exit
      else:
        if nums[i] != int(nums[i]) or nums[j] != int(nums[j]) or target != int(target):
          return 'Неверный тип данных'
          exit
        if nums[i] + nums[j] == target:
          return [i,j]
          break
    return 'Нет решений'
print(two_sum([2,7,11,15],9))
print(2 ** 14)