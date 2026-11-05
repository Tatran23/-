import turtle
import random
import math

def is_in_area(x, y, r1, r2):
    """Проверка попадания точки в заштрихованную область (2 и 4 четверти)"""
    dist_sq = x**2 + y**2
    # Условие принадлежности кольцу
    in_ring = (r2**2 <= dist_sq <= r1**2)
    # Условие принадлежности ко 2-й или 4-й четверти
    in_quads = (x * y <= 0)
    return in_ring and in_quads

def draw_axes(t, x_max, y_max):
    """Рисование осей"""
    t.color("black")
    t.width(2)
    t.penup()
    t.goto(-x_max, 0)
    t.pendown()
    t.goto(x_max, 0)
    t.penup()
    t.goto(0, -y_max)
    t.pendown()
    t.goto(0, y_max)
    
    t.penup()
    t.goto(x_max - 1, -2)
    t.write("X", font=("Arial", 14, "bold"))
    t.goto(-2, y_max - 1)
    t.write("Y", font=("Arial", 14, "bold"))

def main():
    # Параметры фигуры
    R1 = 10.0  # Внешний радиус
    R2 = 5.0   # Внутренний радиус
    N = 10000  # Количество испытаний
    
    # Теоретическая площадь (половина площади кольца)
    S_theory = 0.5 * math.pi * (R1**2 - R2**2)
    
    # Площадь описывающего прямоугольника
    S_box = (2 * R1) * (2 * R1)
    
    # Настройка экрана
    screen = turtle.Screen()
    screen.setup(width=0.8, height=0.8)
    screen.title("Метод Монте-Карло (ЛР №3, Задание 2)")
    screen.tracer(0)
    
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    
    # Установка системы координат
    limit = R1 * 1.2
    screen.setworldcoordinates(-limit, -limit, limit, limit)
    
    draw_axes(t, limit, limit)
    
    # Рисование границ фигуры (для наглядности)
    t.color("gray")
    t.width(2)
    t.penup()
    for r in [R1, R2]:
        t.goto(0, -r)
        t.pendown()
        t.circle(r)
        t.penup()
    
    # Генерация точек
    inside_count = 0
    for _ in range(N):
        x = random.uniform(-R1, R1)
        y = random.uniform(-R1, R1)
        
        if is_in_area(x, y, R1, R2):
            inside_count += 1
            t.color("green")
            t.penup()
            t.goto(x, y)
            t.dot(4)
        # Точки вне области не рисуем для скорости, 
        # но если нужно, можно раскомментировать:
        # else:
        #     t.color("lightcoral")
        #     t.penup()
        #     t.goto(x, y)
        #     t.dot(2)
            
    # Вычисление площади
    S_mc = S_box * (inside_count / N)
    error = abs(S_mc - S_theory) / S_theory * 100
    
    # Вывод результатов на экран
    t.penup()
    t.goto(-limit + 1, limit - 3)
    t.color("black")
    t.write(f"Испытаний: {N}", font=("Arial", 12, "normal"))
    t.goto(-limit + 1, limit - 5)
    t.write(f"Точек внутри: {inside_count}", font=("Arial", 12, "normal"))
    t.goto(-limit + 1, limit - 7)
    t.write(f"Площадь (теория): {S_theory:.2f}", font=("Arial", 12, "normal"))
    t.goto(-limit + 1, limit - 9)
    t.write(f"Площадь (Монте-Карло): {S_mc:.2f}", font=("Arial", 12, "normal"))
    t.goto(-limit + 1, limit - 11)
    t.color("red")
    t.write(f"Погрешность: {error:.2f}%", font=("Arial", 14, "bold"))
    
    screen.update()
    turtle.done()

if __name__ == "__main__":
    main()