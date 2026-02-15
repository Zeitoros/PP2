n = int(input())
nums = [int(x) for x in input().split()][:n]

even_nums = list(filter(lambda x: x % 2 == 0, nums))
print(even_nums)