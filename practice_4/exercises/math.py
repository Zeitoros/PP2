# Exercise 1

import math

degrees = float(input())
rad = degrees * (math.pi / 180)

print(f'{rad:.6f}')


# ----------------------------------------------------------------------


# Exercise 2

a,b,h = map(int, input().split())

area = ((a+b)/2) * h

print(area)


# ----------------------------------------------------------------------


# Exercise 3

from math import tan, pi

sides, length = map(int, input().split())

area = (sides * (length**2)) / (4 * tan(pi/sides))

print(int(area))


# ----------------------------------------------------------------------


# Exercise 4

a,h = map(int, input().split())

area = a * h

print(float(area))