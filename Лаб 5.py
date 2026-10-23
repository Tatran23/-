import random


def generate_matrix(n, m):
    """Генерация матрицы n×m.
    С вероятностью 30 % элемент равен нулю, иначе — случайное число от -3 до 3."""
    matrix = []
    for _ in range(n):
        row = []
        for _ in range(m):
            if random.random() < 0.3:
                row.append(0.0)
            else:
                row.append(float(random.randint(-3, 3)))
        matrix.append(row)
    return matrix


def print_matrix(matrix, title):
    """Вывод матрицы на экран с заголовком."""
    print(title)
    for row in matrix:
        for val in row:
            print("{0: 5.1f}".format(val), end=" ")
        print()
    print()


def compress_matrix(matrix):
    """Удаление нулевых столбцов и строк."""
    if not matrix:
        return []

    n = len(matrix)
    m = len(matrix[0])

    # Индексы столбцов, в которых есть хотя бы один ненулевой элемент
    cols_to_keep = []
    for j in range(m):
        if any(matrix[i][j] != 0.0 for i in range(n)):
            cols_to_keep.append(j)

    # Формируем матрицу только из нужных столбцов
    temp_matrix = []
    for i in range(n):
        new_row = [matrix[i][j] for j in cols_to_keep]
        temp_matrix.append(new_row)

    # Оставляем только строки, где есть хотя бы один ненулевой элемент
    compressed = []
    for row in temp_matrix:
        if any(val != 0.0 for val in row):
            compressed.append(row)

    return compressed


def first_positive_row(matrix):
    """Номер первой строки с положительным элементом (нумерация с 1).
    Если такой строки нет — возвращает None."""
    for i, row in enumerate(matrix):
        if any(val > 0 for val in row):
            return i + 1
    return None


def main():
    # Ввод размеров матрицы
    n = int(input("Введите количество строк N: "))
    m = int(input("Введите количество столбцов M: "))

    if n <= 0 or m <= 0:
        print("Ошибка: размеры матрицы должны быть положительными.")
        return

    # Генерация и вывод исходной матрицы
    matrix = generate_matrix(n, m)
    print_matrix(matrix, "Исходная матрица:")

    # Уплотнение матрицы
    compressed = compress_matrix(matrix)
    print_matrix(compressed, "Уплотнённая матрица:")

    # Поиск первой строки с положительным элементом
    row_num = first_positive_row(compressed)
    if row_num is not None:
        print("Номер первой строки с положительным элементом: {0}".format(row_num))
    else:
        print("Строк с положительными элементами нет.")


if __name__ == "__main__":
    main()