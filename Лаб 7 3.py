# -*- coding: utf-8 -*-
import turtle as tr

# Параметр смещения второй функции
b = float(input("Введите параметр b (например, 0.5): "))

# Точность ряда Тейлора
eps = 1e-4


def taylor_sin_x_over_x(x):
    """sin(x)/x через ряд Тейлора с точностью eps."""
    if abs(x) < 1e-12:
        return 1.0                     # предел при x → 0
    a = 1.0
    y = a
    n = 0
    while True:
        k = -(x**2) / ((2 * n + 2) * (2 * n + 3))
        a *= k
        y += a
        n += 1
        if abs(a) < eps:
            break
    return y


def draw_axes(t, xmin, xmax, ymin, ymax):
    """Рисует оси, деления и подписи."""
    t.color("black")
    t.width(1)

    # Ось X
    t.penup(); t.goto(xmin, 0); t.pendown(); t.goto(xmax, 0)
    t.penup(); t.goto(xmax, 0)
    t.write(" X", font=("Arial", 12, "bold"))

    # Ось Y
    t.penup(); t.goto(0, ymin); t.pendown(); t.goto(0, ymax)
    t.penup(); t.goto(0, ymax)
    t.write(" Y", font=("Arial", 12, "bold"))

    # Метки по оси X
    t.penup()
    for i in range(int(xmin), int(xmax) + 1):
        if i == 0:
            continue
        t.goto(i, 0); t.pendown(); t.goto(i, -0.05); t.penup()
        t.goto(i, -0.17)
        t.write(str(i), align="center", font=("Arial", 8, "normal"))

    # Метки по оси Y
    t.penup()
    for i in range(int(ymin), int(ymax) + 1):
        if i == 0:
            continue
        t.goto(0, i); t.pendown(); t.goto(-0.15, i); t.penup()
        t.goto(-0.55, i - 0.1)
        t.write(str(i), align="right", font=("Arial", 8, "normal"))


def main():
    # Настраиваем экран
    screen = tr.Screen()
    screen.title("Лабораторная №7. График ряда Тейлора (вариант 14)")
    screen.setworldcoordinates(-10, -1, 10, 2)
    screen.tracer(0)                   # отключаем анимацию — рисуем быстро

    # Оси с метками
    draw_axes(tr.Turtle(), -10, 10, -1, 2)

    # Создаём черепашку для графиков
    t = tr.Turtle()
    t.hideturtle()
    t.speed(0)
    t.width(2)

    step = 0.1

    # --- Первая функция: y(x) = sin(x)/x через ряд Тейлора ---
    t.color("blue")
    x = -10.0
    t.penup()
    t.goto(x, taylor_sin_x_over_x(x))
    t.pendown()
    while x <= 10:
        t.goto(x, taylor_sin_x_over_x(x))
        x += step

    # --- Вторая функция: z(x) = y(x) + b ---
    t.color("red")
    x = -10.0
    t.penup()
    t.goto(x, taylor_sin_x_over_x(x) + b)
    t.pendown()
    while x <= 10:
        t.goto(x, taylor_sin_x_over_x(x) + b)
        x += step

    # --- Подписи на полотне ---
    t.color("black")
    t.penup()
    t.goto(-10, 1.9)
    t.write("y(x) = sin(x)/x  (ряд Тейлора, eps = 1e-4)",
            font=("Arial", 10, "bold"))
    t.goto(-10, 1.7)
    t.write("z(x) = sin(x)/x + b,  b = {0:.2f}".format(b),
            font=("Arial", 10, "bold"))

    screen.update()
    screen.exitonclick()


if __name__ == "__main__":
    main()