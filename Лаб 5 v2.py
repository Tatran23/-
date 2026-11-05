import random

def create_matrix(n, m):
    """Создает матрицу n x m со случайными числами от -5 до 5.
    С вероятностью 0.2 элемент равен 0, чтобы могли появиться нулевые строки/столбцы."""
    matrix = []
    for i in range(n):
        row = []
        for j in range(m):
            if random.random() < 0.2:
                row.append(0)
            else:
                row.append(random.randint(-5, 5))
        matrix.append(row)
    return matrix

def print_matrix(matrix, title="Матрица"):
    """Выводит матрицу на экран."""
    print(f"\n{title}:")
    if not matrix:
        print("(пустая матрица)")
        return
    for row in matrix:
        print(" ".join(f"{x:3d}" for x in row))
    print()

def compact_matrix(matrix):
    """Удаляет нулевые строки и столбцы. Возвращает новую матрицу."""
    if not matrix:
        return []
    n = len(matrix)
    m = len(matrix[0])
    
    # Индексы ненулевых строк
    non_zero_rows = []
    for i in range(n):
        if any(x != 0 for x in matrix[i]):
            non_zero_rows.append(i)
    
    # Индексы ненулевых столбцов
    non_zero_cols = []
    for j in range(m):
        if any(matrix[i][j] != 0 for i in range(n)):
            non_zero_cols.append(j)
    
    # Формируем новую матрицу
    new_matrix = []
    for i in non_zero_rows:
        new_row = [matrix[i][j] for j in non_zero_cols]
        new_matrix.append(new_row)
    
    return new_matrix

def find_first_positive_row(matrix):
    """Возвращает номер (1-based) первой строки, содержащей положительный элемент.
    Если такой строки нет, возвращает -1."""
    for i, row in enumerate(matrix):
        if any(x > 0 for x in row):
            return i + 1  # 1-based
    return -1

def main():
    # Запрос размерности
    try:
        n = int(input("Введите количество строк: "))
        m = int(input("Введите количество столбцов: "))
        if n <= 0 or m <= 0:
            print("Размеры должны быть положительными.")
            return
    except ValueError:
        print("Некорректный ввод.")
        return

    # Создание и вывод исходной матрицы
    matrix = create_matrix(n, m)
    print_matrix(matrix, "Исходная матрица")

    # Уплотнение
    compacted = compact_matrix(matrix)
    print_matrix(compacted, "Уплотненная матрица (без нулевых строк и столбцов)")

    # Поиск первой строки с положительным элементом (в исходной матрице)
    row_num = find_first_positive_row(matrix)
    if row_num != -1:
        print(f"Первая строка с положительным элементом (в исходной матрице): {row_num}")
    else:
        print("В исходной матрице нет строк с положительными элементами.")

    # Дополнительно: поиск в уплотненной матрице
    row_num_comp = find_first_positive_row(compacted)
    if row_num_comp != -1:
        print(f"Первая строка с положительным элементом (в уплотненной матрице): {row_num_comp}")
    else:
        print("В уплотненной матрице нет строк с положительными элементами.")

if __name__ == "__main__":
    main()