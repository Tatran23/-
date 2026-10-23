# -*- coding: utf-8 -*-
in_filename = input("Введите имя входного файла (например, in5.txt): ")
out_filename = input("Введите имя выходного файла (например, out5.txt): ")

# --- Чтение исходных данных ---
with open(in_filename, 'r', encoding='utf-8') as f_in:
    N, M = map(int, f_in.readline().split())
    matrix = []
    for _ in range(N):
        row = list(map(float, f_in.readline().split()))
        matrix.append(row)

# --- Уплотнение матрицы ---
# Индексы столбцов, в которых есть хотя бы один ненулевой элемент
cols_to_keep = [j for j in range(M)
                if any(matrix[i][j] != 0.0 for i in range(N))]

# Оставляем только нужные столбцы
temp_matrix = [[matrix[i][j] for j in cols_to_keep] for i in range(N)]

# Оставляем только строки, где есть хотя бы один ненулевой элемент
rows_to_keep = [i for i in range(N)
                if any(temp_matrix[i][j] != 0.0
                       for j in range(len(cols_to_keep)))]
compressed_matrix = [temp_matrix[i] for i in rows_to_keep]

# --- Поиск первой строки с положительным элементом ---
first_pos_row = None
for i, row in enumerate(compressed_matrix, start=1):
    if any(val > 0 for val in row):
        first_pos_row = i
        break

# --- Запись результатов ---
with open(out_filename, 'w', encoding='utf-8') as f_out:
    # Исходная матрица — для сравнения
    f_out.write("Исходная матрица ({}x{}):\n".format(N, M))
    for row in matrix:
        f_out.write(" ".join("{0:6.1f}".format(x) for x in row) + "\n")
    f_out.write("\n")

    # Уплотнённая матрица
    f_out.write("Уплотнённая матрица ({}x{}):\n".format(
        len(compressed_matrix),
        len(compressed_matrix[0]) if compressed_matrix else 0
    ))
    for row in compressed_matrix:
        f_out.write(" ".join("{0:6.1f}".format(x) for x in row) + "\n")
    f_out.write("\n")

    # Номер первой строки с положительным элементом
    if first_pos_row is not None:
        f_out.write("Номер первой строки с положительным элементом: {}\n"
                    .format(first_pos_row))
    else:
        f_out.write("Строк с положительными элементами нет.\n")

print("Результат записан в", out_filename)