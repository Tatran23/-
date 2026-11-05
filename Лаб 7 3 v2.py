import turtle
import math

def taylor_cos(x, eps=1e-3):
    """Вычисление cos(x) с помощью ряда Тейлора"""
    n = 0
    term = 1.0
    total = term
    while abs(term) > eps:
        n += 1
        term *= - (x**2) / ((2*n - 1) * (2*n))
        total += term
    return total

def draw_axes(t, x_min, x_max, y_min, y_max):
    """Рисование осей"""
    t.color("black")
    t.width(2)
    t.penup()
    t.goto(x_min, 0)
    t.pendown()
    t.goto(x_max, 0)
    t.penup()
    t.goto(0, y_min)
    t.pendown()
    t.goto(0, y_max)
    
    # Подписи
    t.penup()
    t.goto(x_max - 0.5, -0.5)
    t.write("X", font=("Arial", 12, "bold"))
    t.goto(-0.5, y_max - 0.5)
    t.write("Y", font=("Arial", 12, "bold"))
    
    # Деления по X (кратные pi/2)
    t.color("gray")
    t.width(1)
    for i in range(int(x_min), int(x_max) + 1):
        if i == 0: continue
        t.goto(i, -0.2)
        t.pendown()
        t.goto(i, 0.2)
        t.penup()
        t.goto(i, -0.5)
        t.write(str(i), align="center", font=("Arial", 8, "normal"))

def main():
    screen = turtle.Screen()
    screen.setup(width=0.8, height=0.8)
    screen.title("Ряд Тейлора cos(x) (ЛР №3, Задание 3)")
    screen.tracer(0)
    
    t = turtle.Turtle()
    t.hideturtle()
    
    x_min, x_max = -10, 10
    y_min, y_max = -2, 2
    
    screen.setworldcoordinates(x_min, y_min, x_max, y_max)
    draw_axes(t, x_min, x_max, y_min, y_max)
    
    # Рисуем идеальный косинус (пунктиром)
    t.penup()
    t.color("gray")
    t.width(1)
    t.goto(x_min, math.cos(x_min))
    t.pendown()
    x = x_min
    while x <= x_max:
        t.goto(x, math.cos(x))
        x += 0.1
    
    # Рисуем график по ряду Тейлора
    t.penup()
    t.color("red")
    t.width(3)
    t.goto(x_min, taylor_cos(x_min))
    t.pendown()
    
    x = x_min
    while x <= x_max:
        y = taylor_cos(x)
        t.goto(x, y)
        x += 0.1
        
    t.penup()
    t.goto(x_min + 1, 1.5)
    t.color("black")
    t.write("График функции cos(x)\n(ряд Тейлора, eps=0.001)", font=("Arial", 10, "normal"))
    
    screen.update()
    turtle.done()

if __name__ == "__main__":
    main()