# -*- coding: utf-8 -*-
import turtle as tr
import random
import math

# Запрашиваем радиус
R = float(input("Введите радиус R: "))

# Настраиваем экран
screen = tr.Screen()
screen.title("Лабораторная №7. Метод Монте-Карло (вариант 14)")
screen.setworldcoordinates(-R - 1, -R - 1, R + 1, R + 1)
screen.tracer(0)          # отключаем анимацию для скорости

# Создаём черепашку
t = tr.Turtle()
t.hideturtle()
t.speed(0)

# ---------- Оси координат ----------
t.color("black")
t.width(1)
# Ось X
t.penup(); t.goto(-R - 0.5, 0); t.pendown(); t.goto(R + 0.5, 0)
t.penup(); t.goto(R + 0.7, -0.5); t.write("X", font=("Arial", 12, "bold"))
# Ось Y
t.penup(); t.goto(0, -R - 0.5); t.pendown(); t.goto(0, R + 0.5)
t.penup(); t.goto(-0.7, R + 0.5); t.write("Y", font=("Arial", 12, "bold"))

# ---------- Контур круга ----------
t.color("blue")
t.width(2)
t.penup()
t.goto(0, -R)
t.pendown()
t.circle(R)

# ---------- Диагональ y = x ----------
t.penup()
t.goto(-R, -R)
t.pendown()
t.goto(R, R)

# ---------- Метод Монте-Карло ----------
N_max = 10000        # число испытаний
N_f = 0              # число попаданий

for _ in range(N_max):
    x = random.uniform(-R, R)
    y = random.uniform(-R, R)

    # Условие попадания в заштрихованную область
    if (x * x + y * y <= R * R) and (x * y >= 0):
        t.penup()
        t.goto(x, y)
        t.dot(3, "green")
        N_f += 1

# ---------- Оценка площади ----------
# Точная площадь: два сектора по 90°, т.е. 1/2 круга
S_real = math.pi * R * R / 2
# Площадь по методу Монте-Карло
S_mc = (2 * R) * (2 * R) * N_f / N_max
# Относительная погрешность
error = abs(S_mc - S_real) / S_real * 100

# ---------- Вывод результатов на полотно ----------
t.color("black")
t.penup()
t.goto(-R, R + 0.5)
t.write("N = {0}".format(N_max), font=("Arial", 11, "bold"))
t.goto(-R, R - 0.3)
t.write("N_f = {0}".format(N_f), font=("Arial", 11, "bold"))
t.goto(-R, R - 1.1)
t.write("S_mc = {0:.4f}".format(S_mc), font=("Arial", 11, "bold"))
t.goto(-R, R - 1.9)
t.write("S_real = {0:.4f}".format(S_real), font=("Arial", 11, "bold"))
t.goto(-R, R - 2.7)
t.write("Ошибка = {0:.2f}%".format(error), font=("Arial", 11, "bold"))

screen.update()

# ---------- Дублируем в консоль ----------
print("Число испытаний: {0}".format(N_max))
print("Точек внутри области: {0}".format(N_f))
print("Площадь методом Монте-Карло: {0:.4f}".format(S_mc))
print("Точная площадь (πR²/4): {0:.4f}".format(S_real))
print("Относительная погрешность: {0:.2f}%".format(error))

# ---------- Завершение ----------
screen.exitonclick()