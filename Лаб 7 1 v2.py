import turtle
import math

def func(x):
    """Кусочно-заданная функция из ЛР №2, Задание 1"""
    if x < -5:
        return 1
    elif -5 <= x < 0:
        return -(3/5) * x - 2
    elif 0 <= x < 2:
        return -math.sqrt(4 - x**2)
    elif 2 <= x < 4:
        return x - 2
    elif 4 <= x < 8:
        return 2 + math.sqrt(4 - (x - 6)**2)
    else:
        return 2

def draw_axes(t, x_min, x_max, y_min, y_max):
    """Рисование осей координат, делений и подписей"""
    t.color("black")
    t.width(2)
    t.penup()
    
    # Ось X
    t.goto(x_min, 0)
    t.pendown()
    t.goto(x_max, 0)
    t.stamp()
    
    # Ось Y
    t.penup()
    t.goto(0, y_min)
    t.pendown()
    t.goto(0, y_max)
    t.stamp()
    
    # Деления и подписи по X
    t.penup()
    t.color("gray")
    t.width(1)
    step_x = 1 if (x_max - x_min) < 30 else 2
    for i in range(int(x_min), int(x_max) + 1, step_x):
        if i == 0: continue
        t.goto(i, -0.3)
        t.pendown()
        t.goto(i, 0.3)
        t.penup()
        if i % 2 == 0: # Подписываем каждое второе
            t.goto(i, -0.8)
            t.write(str(i), align="center", font=("Arial", 8, "normal"))
            
    # Деления и подписи по Y
    for i in range(int(y_min), int(y_max) + 1):
        if i == 0: continue
        t.goto(-0.3, i)
        t.pendown()
        t.goto(0.3, i)
        t.penup()
        t.goto(-0.8, i)
        t.write(str(i), align="right", font=("Arial", 8, "normal"))

def main():
    # Настройка экрана (80% от разрешения экрана)
    screen = turtle.Screen()
    screen.setup(width=0.8, height=0.8)
    screen.title("График функции (ЛР №3, Задание 1)")
    screen.tracer(0)  # Отключаем анимацию для быстрой отрисовки
    
    t = turtle.Turtle()
    t.hideturtle()
    t.shape("arrow")
    
    # Границы графика
    x_min, x_max = -11, 11
    y_min, y_max = -3, 5
    
    # Установка мировой системы координат
    screen.setworldcoordinates(x_min, y_min, x_max, y_max)
    
    # Рисуем оси
    draw_axes(t, x_min, x_max, y_min, y_max)
    
    # Рисуем график функции
    t.color("blue")
    t.width(2)
    t.penup()
    
    step = 0.05
    x = x_min
    first_point = True
    
    while x <= x_max:
        y = func(x)
        
        # Ограничиваем отрисовку видимой областью
        if y_min <= y <= y_max:
            if first_point:
                t.goto(x, y)
                t.pendown()
                first_point = False
            else:
                t.goto(x, y)
        else:
            if not first_point:
                t.penup()
                first_point = True
                
        x += step
    
    # Добавляем подписи осей
    t.penup()
    t.goto(x_max - 0.5, -0.5)
    t.write("X", font=("Arial", 12, "bold"))
    t.goto(-0.5, y_max - 0.5)
    t.write("Y", font=("Arial", 12, "bold"))
    
    screen.update()
    turtle.done()

if __name__ == "__main__":
    main()