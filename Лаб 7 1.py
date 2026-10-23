# -*- coding: utf-8 -*-
import turtle as tr


def f(x):
    """Кусочно-заданная функция (вариант 14)."""
    if x < -4:
        return -2.0
    elif -4 <= x < 0:
        return x**2 / 4 + x
    elif 0 <= x < 2:
        return 2 * x
    else:
        return -0.5 * x + 5


def draw_axes(xmin, xmax, ymin, ymax):
    """Рисует оси, деления и подписи."""
    t = tr.Turtle()
    t.hideturtle()
    t.speed(0)
    t.color("black")
    t.width(1)

    # Ось X
    t.penup()
    t.goto(xmin, 0)
    t.pendown()
    t.goto(xmax, 0)
    t.penup()
    t.goto(xmax, 0)
    t.write(" X", font=("Arial", 12, "bold"))

    # Ось Y
    t.penup()
    t.goto(0, ymin)
    t.pendown()
    t.goto(0, ymax)
    t.penup()
    t.goto(0, ymax)
    t.write(" Y", font=("Arial", 12, "bold"))

    # Деления и подписи по оси X
    t.penup()
    for i in range(int(xmin), int(xmax) + 1):
        if i == 0:
            continue
        t.goto(i, 0)
        t.pendown()
        t.goto(i, -0.2)
        t.penup()
        t.goto(i, -0.7)
        t.write(str(i), align="center", font=("Arial", 8, "normal"))

    # Деления и подписи по оси Y
    t.penup()
    for i in range(int(ymin), int(ymax) + 1):
        if i == 0:
            continue
        t.goto(0, i)
        t.pendown()
        t.goto(-0.2, i)
        t.penup()
        t.goto(-0.7, i - 0.2)
        t.write(str(i), align="right", font=("Arial", 8, "normal"))


def main():
    # Создаём экран
    screen = tr.Screen()
    screen.title("Лабораторная №7. График функции (вариант 14)")
    screen.setworldcoordinates(-10, -5, 10, 10)
    screen.tracer(0)  # отключаем анимацию — рисуем быстро

    # Оси с метками
    draw_axes(-10, 10, -5, 10)

    # Рисуем график функции
    t = tr.Turtle()
    t.hideturtle()
    t.speed(0)
    t.color("green")
    t.width(2)

    x = -10
    t.penup()
    t.goto(x, f(x))
    t.pendown()

    step = 0.05
    while x <= 10:
        t.goto(x, f(x))
        x += step

    screen.update()       # показываем всё нарисованное
    screen.exitonclick()  # окно закрывается по клику


if __name__ == "__main__":
    main()