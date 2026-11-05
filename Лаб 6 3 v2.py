import sys

def read_matrix_from_file(filename):
    """
    Читает размерность и матрицу из файла.
    Формат файла:
    Первая строка: n m (количество строк и столбцов)
    Далее n строк по m целых чисел.
    Возвращает (n, m, matrix).
    """
    try:
        with open(filename, 'r') as f:
            first_line = f.readline().strip()
            if not first_line:
                raise ValueError("Файл пуст или первая строка пуста")
            n, m = map(int, first_line.split())
            if n <= 0 or m <= 0:
                raise ValueError("Размеры матрицы должны быть положительными")
            matrix = []
            for i in range(n):
                line = f.readline().strip()
                if not line:
                    raise ValueError(f"Недостаточно строк в файле: ожидалось {n}, получено {i}")
                row = list(map(int, line.split()))
                if len(row) != m:
                    raise ValueError(f"В строке {i+1} ожидалось {m} чисел, получено {len(row)}")
                matrix.append(row)
            return n, m, matrix
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка чтения файла: {e}", file=sys.stderr)
        sys.exit(1)

def write_results_to_file(filename, original, compacted, row_num_original, row_num_compacted):
    """
    Записывает результаты в файл:
    - исходная матрица
    - уплотнённая матрица
    - номер первой строки с положительным элементом (в исходной и уплотнённой)
    """
    with open(filename, 'w') as f:
        f.write("Исходная матрица:\n")
        for row in original:
            f.write(" ".join(f"{x:3d}" for x in row) + "\n")
        f.write("\n")
        
        f.write("Уплотнённая матрица (без нулевых строк и столбцов):\n")
        if compacted:
            for row in compacted:
                f.write(" ".join(f"{x:3d}" for x in row) + "\n")
        else:
            f.write("(пустая матрица)\n")
        f.write("\n")
        
        if row_num_original != -1:
            f.write(f"Первая строка с положительным элементом (в исходной матрице): {row_num_original}\n")
        else:
            f.write("В исходной матрице нет строк с положительными элементами.\n")
        
        if row_num_compacted != -1:
            f.write(f"Первая строка с положительным элементом (в уплотнённой матрице): {row_num_compacted}\n")
        else:
            f.write("В уплотнённой матрице нет строк с положительными элементами.\n")

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
            return i + 1
    return -1

def main():
    input_file = "input.txt"
    output_file = "output.txt"
    
    # Чтение данных из файла
    n, m, matrix = read_matrix_from_file(input_file)
    
    # Обработка
    compacted = compact_matrix(matrix)
    row_num_original = find_first_positive_row(matrix)
    row_num_compacted = find_first_positive_row(compacted)
    
    # Запись результатов в файл
    write_results_to_file(output_file, matrix, compacted, row_num_original, row_num_compacted)
    
    print(f"Результаты записаны в файл {output_file}")

if __name__ == "__main__":
    main()