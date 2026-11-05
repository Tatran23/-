import turtle as tr

# Функция, вычисляющая Y по заданному X
def my_func(x):
    if x <= -4:
        return -2
    elif -4 < x <= 0:
        return 0.25 * x
    elif 0 < x <= 2:
        return x**2
    else:
        return -0.5 * x + 5

# --- Настройка окна и системы координат ---
tr.setup(800, 500)
# Устанавливаем мировые координаты: (x_min, y_min, x_max, y_max)
# Берем с небольшим запасом, чтобы график не упирался в края
tr.setworldcoordinates(-7, -3, 13, 5) 
tr.title("Лабораторная работа №7. Вариант 14")
tr.speed(0) # Максимальная скорость рисования
tr.hideturtle() # Скрываем черепашку

# --- Рисование осей ---
def draw_axes():
    tr.penup()
    tr.goto(-7, 0)
    tr.pendown()
    tr.goto(13, 0) # Ось X
    
    tr.penup()
    tr.goto(0, -3)
    tr.pendown()
    tr.goto(0, 5)  # Ось Y
    
    # Стрелки на осях можно добавить отдельно, но для базовой сдачи хватит и линий
    
    # Подписи осей
    tr.penup()
    tr.goto(12.5, -0.5)
    tr.write("X", font=("Arial", 14))
    tr.goto(0.2, 4.5)
    tr.write("Y", font=("Arial", 14))

draw_axes()

# --- Рисование графика ---
tr.penup()
tr.color("blue") # Цвет графика
tr.width(2)      # Толщина линии

# Начальная точка
start_x = -6
start_y = my_func(start_x)
tr.goto(start_x, start_y)
tr.pendown()

# Шаг для плавности
dx = 0.05
x = start_x

while x <= 12:
    y = my_func(x)
    tr.goto(x, y)
    x += dx

# Чтобы окно не закрылось сразу
tr.done()