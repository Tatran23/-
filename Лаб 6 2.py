# -*- coding: utf-8 -*-
in_filename = input("Введите имя входного файла (например, in4.txt): ")
out_filename = input("Введите имя выходного файла (например, out4.txt): ")

# --- Чтение исходных данных ---
with open(in_filename, 'r', encoding='utf-8') as f_in:
    N = int(f_in.readline().strip())
    arr = []
    for _ in range(N):
        arr.append(float(f_in.readline().strip()))

# --- Обработка ---
# 1. Количество нулевых элементов (с учётом погрешности float)
count_zeros = sum(1 for val in arr if abs(val) < 1e-7)

# 2. Индекс минимального элемента и сумма после него
min_idx = arr.index(min(arr))
min_value = arr[min_idx]
sum_after = sum(arr[min_idx + 1:])

# 3. Сортировка по возрастанию модулей
arr_sorted = sorted(arr, key=abs)

# --- Запись результатов ---
with open(out_filename, 'w', encoding='utf-8') as f_out:
    # Исходный массив — чтобы было с чем сравнивать
    f_out.write("Исходный массив (N = {}):\n".format(N))
    f_out.write(" ".join("{0:.4f}".format(x) for x in arr) + "\n\n")

    # 1. Количество нулей
    f_out.write("1. Количество нулевых элементов: {}\n".format(count_zeros))

    # 2. Минимум и сумма после него
    f_out.write("2. Минимальный элемент: arr[{}] = {:.4f}\n".format(min_idx, min_value))
    f_out.write("   Сумма элементов после минимального: {:.4f}\n".format(sum_after))

    # 3. Отсортированный по модулю массив
    f_out.write("3. Массив, упорядоченный по возрастанию модулей:\n")
    f_out.write(" ".join("{0:.4f}".format(x) for x in arr_sorted) + "\n")

print("Результат записан в", out_filename)