import math

in_filename = input("Введите имя входного файла (например, in1.txt): ")
out_filename = input("Введите имя выходного файла (например, out1.txt): ")

# Читаем все непустые строки из входного файла — каждая строка содержит одно значение x
with open(in_filename, 'r', encoding='utf-8') as f_in:
    x_values = []
    for line in f_in:
        line = line.strip()
        if line:                      # пропускаем пустые строки
            x_values.append(float(line))

# Открываем файл для записи и формируем таблицу результатов
with open(out_filename, 'w', encoding='utf-8') as f_out:
    f_out.write("+----------+------------+------------+\n")
    f_out.write("|    X     |     Z1     |     Z2     |\n")
    f_out.write("+----------+------------+------------+\n")

    for x in x_values:
        cos_x = math.cos(x)
        sin_x = math.sin(x)
        cos_2x = math.cos(2 * x)

        # z1 = (cos x + sin x) / (cos x - sin x)
        if abs(cos_x - sin_x) < 1e-12:
            z1_str = "   error  "
        else:
            z1 = (cos_x + sin_x) / (cos_x - sin_x)
            z1_str = f"{z1:10.4f}"

        # z2 = tg(2x) + 1 / cos(2x)
        if abs(cos_2x) < 1e-12:
            z2_str = "   error  "
        else:
            z2 = math.tan(2 * x) + 1 / cos_2x
            z2_str = f"{z2:10.4f}"

        f_out.write(f"| {x:8.4f} | {z1_str} | {z2_str} |\n")

    f_out.write("+----------+------------+------------+\n")

print("Результат записан в", out_filename)