import tkinter as tk
import os

# Именованная константа: количество столбцов
N_BARS = 5
DATA_FILE = "chart_data.txt"

def create_sample_data():
    """Создает текстовый файл с примером данных (если файла нет)"""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write("# Категория Значение_2022 Значение_2023\n")
            f.write("Товар A 15 22\n")
            f.write("Товар B 28 35\n")
            f.write("Товар C 10 18\n")
            f.write("Товар D 35 40\n")
            f.write("Товар E 20 25\n")

def read_data(filename):
    """Чтение данных из файла (исправленная версия)"""
    categories = []
    values1 = []
    values2 = []
    
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            # Пропускаем комментарии и пустые строки
            if line.startswith("#") or not line.strip():
                continue
                
            parts = line.split()
            if len(parts) >= 3 and len(categories) < N_BARS:
                try:
                    # Последние два элемента - это числа. Всё, что до них - название категории.
                    val2 = float(parts[-1])
                    val1 = float(parts[-2])
                    cat_name = " ".join(parts[:-2])  # Объединяем оставшиеся слова обратно в строку
                    
                    values1.append(val1)
                    values2.append(val2)
                    categories.append(cat_name)
                except ValueError:
                    print(f"Предупреждение: не удалось прочитать строку: {line.strip()}")
                    continue
                
    return categories, values1, values2

def draw_bar_chart(canvas, x, y, w, h, data, labels, title, x_label, y_label, max_val):
    """Процедура рисования одной столбиковой диаграммы"""
    if w <= 0 or h <= 0:
        return
        
    # 1. Рисуем заголовок и подписи осей
    canvas.create_text(x + w / 2, y - 25, text=title, font=("Arial", 14, "bold"))
    canvas.create_text(x + w / 2, y + h + 40, text=x_label, font=("Arial", 11))
    canvas.create_text(x - 45, y + h / 2, text=y_label, font=("Arial", 11), angle=90)

    # 2. Рисуем оси координат
    canvas.create_line(x, y, x, y + h, width=2)          # Ось Y
    canvas.create_line(x, y + h, x + w, y + h, width=2)  # Ось X

    # 3. Рисуем разметку и подписи по оси Y (градации)
    steps = 5
    for i in range(steps + 1):
        val = max_val * i / steps
        py = y + h - (val / max_val) * h
        canvas.create_line(x - 5, py, x, py, width=1)
        canvas.create_text(x - 15, py, text=f"{val:.1f}", anchor="e", font=("Arial", 9))

    # 4. Рисуем столбцы
    n = len(data)
    if n == 0:
        return
        
    bar_width = w / n
    gap = bar_width * 0.15 # Отступ между столбцами

    for i in range(n):
        # Вычисляем координаты столбца
        val = data[i]
        bar_h = (val / max_val) * h if max_val > 0 else 0
        
        x1 = x + i * bar_width + gap
        y1 = y + h - bar_h
        x2 = x + (i + 1) * bar_width - gap
        y2 = y + h
        
        # Рисуем прямоугольник (столбец)
        color = "#4da6ff" if i % 2 == 0 else "#66b3ff"
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        
        # Подпись под столбцом (ось X)
        canvas.create_text((x1 + x2) / 2, y + h + 15, text=labels[i], font=("Arial", 10), justify="center")

def on_resize(event, canvas, cats, v1, v2):
    """Функция для перерисовки при изменении размера окна"""
    canvas.delete("all") # Очищаем холст
    
    width = event.width
    height = event.height
    
    # Отступы от краев экрана
    padding = 80
    available_w = width - 3 * padding
    available_h = height - 2 * padding
    
    if available_w <= 0 or available_h <= 0:
        return
        
    # Общий максимум для обеих диаграмм, чтобы масштаб был одинаковым
    global_max = max(max(v1), max(v2))
    if global_max <= 0:
        global_max = 1.0 
        
    # Ширина одной диаграммы
    chart_w = available_w / 2
    
    # Рисуем левую диаграмму
    draw_bar_chart(
        canvas, 
        x=padding, 
        y=padding, 
        w=chart_w, 
        h=available_h, 
        data=v1, 
        labels=cats, 
        title="Продажи 2022", 
        x_label="Товары", 
        y_label="Количество, шт.", 
        max_val=global_max
    )
    
    # Рисуем правую диаграмму
    draw_bar_chart(
        canvas, 
        x=padding * 2 + chart_w, 
        y=padding, 
        w=chart_w, 
        h=available_h, 
        data=v2, 
        labels=cats, 
        title="Продажи 2023", 
        x_label="Товары", 
        y_label="Количество, шт.", 
        max_val=global_max
    )

def main():
    # Подготовка данных
    create_sample_data()
    categories, values1, values2 = read_data(DATA_FILE)
    
    if not categories:
        print("Ошибка: файл данных пуст или имеет неверный формат.")
        return

    # Настройка главного окна
    root = tk.Tk()
    root.title("ЛР №8 - Столбиковые диаграммы")
    
    # Занимаем 80% экрана
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    win_w = int(screen_w * 0.8)
    win_h = int(screen_h * 0.8)
    
    root.geometry(f"{win_w}x{win_h}")
    root.minsize(600, 400)
    
    # Создание холста
    canvas = tk.Canvas(root, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Привязка события изменения размера окна
    canvas.bind("<Configure>", lambda event: on_resize(event, canvas, categories, values1, values2))
    
    root.mainloop()

if __name__ == "__main__":
    main()