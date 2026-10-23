import random

N = int(input("Введите количество элементов массива N: "))

# Проверка корректности ввода
if N <= 0:
    print("Ошибка: количество элементов должно быть больше нуля.")
    exit()

# Создаем пустой список и заполняем его случайными числами от -10 до 10
arr = []
for _ in range(N):
    arr.append(random.uniform(-10, 10))

# Выводим исходный массив
print("\nИсходный массив:")
for val in arr:
    print("{0: .4f}".format(val), end=" ")
print()

# 1. Считаем количество элементов, равных нулю (с учётом погрешности float)
count_zeros = 0
for val in arr:
    if abs(val) < 1e-7:      # если модуль очень мал, считаем элемент нулевым
        count_zeros += 1
print("\n1. Количество нулевых элементов: {0}".format(count_zeros))

# 2. Находим индекс минимального элемента
min_idx = 0
for i in range(1, N):
    if arr[i] < arr[min_idx]:
        min_idx = i

# Считаем сумму элементов, расположенных после минимального
sum_after = 0.0
for i in range(min_idx + 1, N):
    sum_after += arr[i]

print("2. Минимальный элемент: arr[{0}] = {1: .4f}".format(min_idx, arr[min_idx]))
print("   Сумма элементов после минимального: {0: .4f}".format(sum_after))

# 3. Сортируем массив по возрастанию модулей (ключ сортировки — abs)
arr.sort(key=abs)

# Выводим отсортированный массив
print("\n3. Массив, упорядоченный по возрастанию модулей:")
for val in arr:
    print("{0: .4f}".format(val), end=" ")
print()