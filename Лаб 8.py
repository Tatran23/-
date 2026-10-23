# -*- coding: utf-8 -*-
import os
import math
import tkinter as tk

# ---------------- Именованные константы ----------------
NUM_BARS      = 6                # количество столбцов (поставщиков)
CANVAS_W      = 720              # ширина одного полотна
CANVAS_H      = 520              # высота одного полотна

MARGIN_LEFT   = 80               # место под подписи оси Y
MARGIN_RIGHT  = 30
MARGIN_TOP    = 90               # заголовок + легенда
MARGIN_BOTTOM = 90               # подписи оси X

N_TICKS_Y     = 10               # число делений по оси Y

COLOR_1996    = "#3a7bd5"        # синий
COLOR_1995    = "#d9534f"        # красный
GRID_COLOR    = "#e0e0e0"
AXIS_COLOR    = "black"
TEXT_COLOR    = "#222222"

FONT_TITLE    = ("Arial", 14, "bold")
FONT_LABEL    = ("Arial", 11, "bold")
FONT_TICK     = ("Arial", 9)
FONT_VALUE    = ("Arial", 8)
FONT_LEGEND   = ("Arial", 9)


# ---------------- Вспомогательные функции ----------------
def nice_max(value):
    """Возвращает «круглое» число чуть больше value — для верхней границы оси Y."""
    if value <= 0:
        return 1
    exp  = math.floor(math.log10(value))
    base = 10 ** exp
    for k in (1, 2, 2.5, 5, 10):
        if value <= k * base:
            return k * base
    return 10 * base


def read_data(filename, n):
    """Читает n строк из файла.
    Возвращает два списка: names, rows. rows[i] = (v1996, v1995)."""
    names, v1996, v1995 = [], [], []
    with open(filename, "r", encoding="utf-8") as f:
        for _ in range(n):
            line = f.readline().strip()
            if not line:
                break
            parts = line.split()
            if len(parts) < 5:
                continue
            names.append(parts[0])
            v1996.append(float(parts[1]))
            v1995.append(float(parts[3]))
    return names, v1996, v1995


def draw_axes(canvas, x0, y0, w, h, y_max, ylabel, xlabel):
    """Рисует оси, сетку, деления и подписи осей."""
    # Сетка по Y (тонкие горизонтальные линии)
    for i in range(1, N_TICKS_Y + 1):
        ypix = y0 - h * i / N_TICKS_Y
        canvas.create_line(x0, ypix, x0 + w, ypix,
                           fill=GRID_COLOR, dash=(2, 4))

    # Оси
    canvas.create_line(x0, y0, x0, y0 - h, width=2,
                       fill=AXIS_COLOR, arrow=tk.LAST)
    canvas.create_line(x0, y0, x0 + w, y0, width=2,
                       fill=AXIS_COLOR, arrow=tk.LAST)

    # Деления и подписи по Y
    for i in range(N_TICKS_Y + 1):
        val  = y_max * i / N_TICKS_Y
        ypix = y0 - h * i / N_TICKS_Y
        canvas.create_line(x0 - 5, ypix, x0, ypix, fill=AXIS_COLOR)
        canvas.create_text(x0 - 8, ypix, text=f"{val:.0f}",
                           anchor="e", fill=TEXT_COLOR, font=FONT_TICK)

    # Подписи осей
    canvas.create_text(x0 + w // 2, y0 + 60, text=xlabel,
                       fill=TEXT_COLOR, font=FONT_LABEL)
    canvas.create_text(x0 - 55, y0 - h // 2, text=ylabel, angle=90,
                       fill=TEXT_COLOR, font=FONT_LABEL)


def draw_legend(canvas, x, y):
    """Небольшая легенда в правом верхнем углу полотна."""
    size = 14

    canvas.create_rectangle(x, y, x + size, y + size,
                            fill=COLOR_1996, outline=AXIS_COLOR)
    canvas.create_text(x + size + 6, y + size / 2, text="1996 г.",
                       anchor="w", fill=TEXT_COLOR, font=FONT_LEGEND)

    canvas.create_rectangle(x, y + size + 6, x + size, y + 2 * size + 6,
                            fill=COLOR_1995, outline=AXIS_COLOR)
    canvas.create_text(x + size + 6, y + 1.5 * size + 6, text="1995 г.",
                       anchor="w", fill=TEXT_COLOR, font=FONT_LEGEND)


def draw_grouped_bars(canvas, title, xlabel, ylabel,
                      names, v1996, v1995):
    """Процедура построения сгруппированной столбиковой диаграммы."""
    canvas.delete("all")

    # Заголовок
    canvas.create_text(CANVAS_W // 2, 25, text=title,
                       fill=TEXT_COLOR, font=FONT_TITLE)

    # Внутренняя область графика
    x0 = MARGIN_LEFT
    y0 = CANVAS_H - MARGIN_BOTTOM
    w  = CANVAS_W - MARGIN_LEFT - MARGIN_RIGHT
    h  = CANVAS_H - MARGIN_TOP - MARGIN_BOTTOM

    y_max = nice_max(max(max(v1996), max(v1995)))

    # Оси и сетка
    draw_axes(canvas, x0, y0, w, h, y_max, ylabel, xlabel)

    # Легенда в правом верхнем углу
    draw_legend(canvas, CANVAS_W - MARGIN_RIGHT - 110, 10)

    # Столбцы
    n       = len(names)
    group_w = w / n
    bar_w   = group_w * 0.32

    for i in range(n):
        cx = x0 + group_w * i + group_w / 2

        # Столбец 1996
        y1 = y0 - h * v1996[i] / y_max
        canvas.create_rectangle(cx - bar_w, y1, cx, y0,
                                fill=COLOR_1996, outline="")
        canvas.create_text(cx - bar_w / 2, y1 - 8,
                           text=f"{v1996[i]:.0f}",
                           fill=TEXT_COLOR, font=FONT_VALUE)

        # Столбец 1995
        y2 = y0 - h * v1995[i] / y_max
        canvas.create_rectangle(cx, y2, cx + bar_w, y0,
                                fill=COLOR_1995, outline="")
        canvas.create_text(cx + bar_w / 2, y2 - 8,
                           text=f"{v1995[i]:.0f}",
                           fill=TEXT_COLOR, font=FONT_VALUE)

        # Подпись поставщика
        canvas.create_text(cx, y0 + 18, text=names[i], angle=90,
                           fill=TEXT_COLOR, font=("Arial", 9))


# ---------------- Основная программа ----------------
def main():
    filename = input("Введите имя файла с данными (например, lab8_in.txt): ")

    # Автосоздание тестового файла
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Compaq   7036 10.3  5757  9.8\n")
            f.write("IBM      6081  8.9  4785  8.1\n")
            f.write("Packard  4247  6.2  4392  7.5\n")
            f.write("Bell_NEC 3587  5.2  4627  7.9\n")
            f.write("Apple    2995  4.4  2023  3.4\n")
            f.write("HP       4459 65.0  7221 63.3\n")
        print("Создан тестовый файл:", filename)

    # Чтение данных (две пары: объёмы и доли)
    names, vol1996, vol1995 = read_data(filename, NUM_BARS)
    _,      shr1996, shr1995 = read_data(filename, NUM_BARS)

    # Главное окно
    root = tk.Tk()
    root.title("Лабораторная №8, вариант 14 — две столбиковые диаграммы")
    root.resizable(False, False)

    # Два холста рядом
    cv1 = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H,
                    bg="white", highlightthickness=1,
                    highlightbackground="#cccccc")
    cv1.pack(side=tk.LEFT, padx=10, pady=10)

    cv2 = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H,
                    bg="white", highlightthickness=1,
                    highlightbackground="#cccccc")
    cv2.pack(side=tk.LEFT, padx=10, pady=10)

    # Первая диаграмма — объём продаж
    draw_grouped_bars(cv1,
                      title="Объём продаж ПК",
                      xlabel="Поставщик",
                      ylabel="Тыс. шт.",
                      names=names,
                      v1996=vol1996,
                      v1995=vol1995)

    # Вторая диаграмма — доля рынка
    draw_grouped_bars(cv2,
                      title="Доля рынка ПК",
                      xlabel="Поставщик",
                      ylabel="Проценты, %",
                      names=names,
                      v1996=shr1996,
                      v1995=shr1995)

    root.mainloop()


if __name__ == "__main__":
    main()