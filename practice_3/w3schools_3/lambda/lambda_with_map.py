n = int(input())
nums = [int(x) for x in input().split()][:n]

squared = list(map(lambda x: x**2, nums))
print(squared)