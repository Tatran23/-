from datetime import datetime, timedelta

# Список сторон света в порядке возрастания угла:
# индекс 0 — север (0°), индекс 4 — восток (90°),
# индекс 8 — юг (180°), индекс 12 — запад (270°).
COMPASS_POINTS = [
    "С", "ССВ", "СВ", "ВСВ", "В", "ВЮВ", "ЮВ", "ЮЮВ",
    "Ю", "ЮЮЗ", "ЮЗ", "ЗЮЗ", "З", "ЗСЗ", "СЗ", "ССЗ",
]


def degrees_to_compass(raw_degrees):
    """Преобразует угол ветра в градусах в обозначение стороны света."""
    # Приводим значение к int: API может прислать строку или число.
    try:
        angle = int(raw_degrees)
    except (ValueError, TypeError):
        # Если данные некорректны — возвращаем понятную ошибку,
        # чтобы вызывающий код не падал на арифметике.
        return "Ошибка формата данных о направлении ветра от API!"

    # Каждая сторона света занимает сектор 22.5°.
    # Прибавляем половину сектора (11.25°), чтобы 0° попадал
    # в центр сектора "С", а не на границу между "ССЗ" и "С".
    # Деление на 22.5 даёт номер сектора, остаток от 16
    # защищает от отрицательных или слишком больших углов.
    step = int((angle + 11.25) // 22.5) % len(COMPASS_POINTS)
    return COMPASS_POINTS[step]


def epoch_to_readable_time(raw_epoch, raw_offset):
    """Преобразует unix-время и смещение часового пояса в читаемое локальное время."""
    # Unix-время от API приходит как число секунд с 01.01.1970 UTC.
    try:
        epoch = int(raw_epoch)
    except (ValueError, TypeError):
        return "Ошибка формата данных о восходе/закате от API!"

    # Смещение часового пояса тоже приходит числом секунд
    # относительно UTC (например, 10800 = UTC+3 для Москвы).
    try:
        offset = int(raw_offset)
    except (ValueError, TypeError):
        return "Ошибка формата данных о часовом поясе от API!"

    # utcfromtimestamp даёт время в UTC,
    # прибавление offset переводит его в локальное время города.
    local = datetime.utcfromtimestamp(epoch) + timedelta(seconds=offset)
    return local.strftime("%Y-%m-%d %H:%M:%S")


def kelvin_to_unit(raw_kelvin, unit):
    """Переводит температуру из Кельвинов в Цельсий или Фаренгейт."""
    # OpenWeatherMap всегда отдаёт температуру в Кельвинах.
    try:
        kelvin = float(raw_kelvin)
    except (ValueError, TypeError):
        return "Ошибка формата данных о температуре от API!"

    # Нормализуем единицу измерения, чтобы 'c' и 'C' работали одинаково.
    unit = str(unit).upper()
    if unit not in ("C", "F"):
        return "Единица температуры должна быть 'C' или 'F'!"

    # Формулы перевода из Кельвинов.
    if unit == "C":
        return f"{kelvin - 273.15:.2f} °C"
    return f"{kelvin * 9 / 5 - 459.67:.2f} °F"