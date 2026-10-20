from math import *

alpha = float(input("Введите значение угла альфа (в радианах): "))

z1 = (cos(alpha) + sin(alpha)) / (cos(alpha) - sin(alpha))

# sec(2a) заменяем на 1 / cos(2a)
z2 = tan(2 * alpha) + 1 / cos(2 * alpha)

print("z1 = {0:.4f}   z2 = {1:.4f}".format(z1, z2))