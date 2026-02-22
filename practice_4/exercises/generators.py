# Exercise #1

def squares(n):
    for i in range(1, n+1):
        i = i**2
        yield i
        
n = int(input())
for i in squares(n):
    print(i)


# ----------------------------------------------------------------------


# Exercise #2

def even(n):
    for i in range(n+1):
        if i % 2 == 0:
            yield i

n = int(input())
first = True
for i in even(n):
    if not first:
        print(',', end='')
    print(i, end='')
    first = False


# ------------------------------------------------------------------------


# Exercise 3

def div(n):
    for i in range(0, n+1, 12):
        yield i

n = int(input())

for i in div(n):
    print(i)


# ----------------------------------------------------------------------


# Exercise 4

def squares_a_b(a,b):
    for i in range(a, b+1):
        i = i**2
        yield i
        
a, b = map(int, input().split())

for i in squares_a_b(a, b):
    print(i)


# ----------------------------------------------------------------------


# Exercise 5

def countdown(n):
    for i in range(n, -1, -1):
        yield i
        
n = int(input())

for i in countdown(n):
    print(i)