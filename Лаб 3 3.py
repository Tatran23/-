from math import fabs


def main():
    X_beg = float(input("Введите Xbeg: "))
    X_end = float(input("Введите Xend: "))
    dx = float(input("Введите шаг dx: "))
    eps = float(input("Введите точность eps: "))

    if dx == 0:
        print("Ошибка: dx не должен быть равен 0.")
        return

    if (X_end - X_beg) * dx < 0:
        print("Ошибка: шаг dx должен вести от Xbeg к Xend.")
        return

    if eps <= 0:
        print("Ошибка: eps должно быть больше 0.")
        return

    print("+----------+------------+------+")
    print("|    X     |     Y      |  N   |")
    print("+----------+------------+------+")

    xt = X_beg

    # Цикл работает и при положительном, и при отрицательном dx
    while ((dx > 0 and xt <= X_end + 1e-12) or
           (dx < 0 and xt >= X_end - 1e-12)):

        # Первый член ряда: a0 = 1
        a = 1.0
        y = a

        # n — индекс текущего члена ряда
        n = 0

        while True:
            # Переход от a_n к a_{n+1}
            # Для cos(x): a_{n+1} = -a_n * x^2 / ((2n+1)(2n+2))
            k = -(xt * xt) / ((2 * n + 1) * (2 * n + 2))
            a = a * k
            y = y + a
            n += 1

            if fabs(a) < eps:
                break

        # n + 1 — количество просуммированных членов, включая a0
        print("| {0:8.4f} | {1:10.6f} | {2:4d} |".format(xt, y, n + 1))

        xt += dx

    print("+----------+------------+------+")


if __name__ == "__main__":
    main()