# filter()

nums = list(range(1,21))
even_nums = list(filter((lambda x: x%2==0), nums))
print(even_nums)



# map()

nums = list(range(1,11))
triple = list(map((lambda x: 3*x), nums))
print(triple)



# reduce()

from functools import reduce

nums = [47, 11, 42, 102, 13]
max_value = reduce(lambda x,y: x if x>y else y, nums)
print(max_value)