import requests
from datetime import datetime
from weather_tools import (
    degrees_to_compass,
    epoch_to_readable_time,
    kelvin_to_unit,
)

# Базовый адрес эндпоинта OpenWeatherMap для текущей погоды.
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"

# Имя файла, в который сохраняется отчёт.
OUTPUT_FILE = "weatherinfo.txt"


def request_weather(api_key, city):
    """Запрашивает у OpenWeatherMap текущую погоду в городе."""
    try:
        # Параметры передаём словарём: requests сам кодирует
        # пробелы и спецсимволы в названии города,
        # поэтому не нужно вручную собирать URL.
        response = requests.get(
            API_ENDPOINT,
            params={"q": city, "appid": api_key},
            timeout=10,  # чтобы программа не висела при проблемах с сетью
        )
        # .json() сразу разбирает ответ в словарь Python.
        return response.json()
    except requests.exceptions.RequestException as error:
        # Сюда попадают ошибки сети, таймауты, DNS и т.п.
        print(f"Ошибка при получении данных о погоде: {error}")
        return None


def api_error_message(payload):
    """Возвращает понятное пользователю сообщение, если API вернул код ошибки."""
    # OpenWeatherMap сообщает об ошибках через поле "cod":
    # "401" — неверный ключ, "404" — город не найден.
    code = str(payload.get("cod", ""))
    if code == "401":
        return "Неверный API-ключ. Проверьте ключ и попробуйте снова."
    if code == "404":
        return (
            "Город не найден. Проверьте название и код страны.\n"
            "Формат: 'Город,CC', где CC — двухбуквенный код страны "
            "по стандарту ISO 3166-1 alpha-2 (например, RU, US, DE).\n"
            "Примеры: 'Moscow,RU', 'London,GB', 'New York,US'."
        )
    # Всё остальное (включая успешный код 200) — не ошибка.
    return None


def format_report(payload, unit):
    """Формирует список строк с отчётом о текущей погоде."""
    lines = []
    # Локальные дата и время запуска — для шапки отчёта.
    stamp = datetime.now().strftime("%d.%m.%Y | %H:%M:%S")

    # Блок sys содержит страну, восход и закат.
    sys_block = payload.get("sys", {})
    city = payload.get("name")
    country = sys_block.get("country")

    # Шапку пишем, только если API вернул и город, и страну.
    if city and country:
        lines.append("-" * 61)
        lines.append(f"Погода для - {city} | {country} | {stamp}")
        lines.append("-" * 61)

    # Блок main содержит температуру, влажность и т.п.
    main = payload.get("main", {})
    if "temp" in main:
        lines.append(
            f"\tТекущая температура     : {kelvin_to_unit(main['temp'], unit)}"
        )

    # weather — список; на практике всегда один элемент,
    # но проверяем на пустоту, чтобы не упасть на weather[0].
    weather = payload.get("weather") or []
    if weather:
        lines.append(f"\tОписание погоды         : {weather[0]['description']}")

    if "humidity" in main:
        lines.append(f"\tВлажность               : {main['humidity']} %")

    # Блок wind содержит скорость и угол ветра.
    wind = payload.get("wind", {})
    if "speed" in wind:
        lines.append(f"\tСкорость ветра          : {wind['speed']} км/ч")

    if "deg" in wind:
        lines.append(
            f"\tНаправление ветра       : {degrees_to_compass(wind['deg'])}"
        )

    # Время восхода/заката хранится в sys как unix-время,
    # а смещение часового пояса — в корне ответа (timezone).
    tz = payload.get("timezone")
    if "sunrise" in sys_block and tz is not None:
        lines.append(
            "\tВремя восхода сегодня   : "
            + epoch_to_readable_time(sys_block["sunrise"], tz)
        )

    if "sunset" in sys_block and tz is not None:
        lines.append(
            "\tВремя заката сегодня    : "
            + epoch_to_readable_time(sys_block["sunset"], tz)
        )

    return lines


def save_report(lines, filename=OUTPUT_FILE):
    """Сохраняет собранный отчёт в текстовый файл."""
    try:
        # encoding="utf-8" обязателен: иначе на Windows
        # кириллица в файле превратится в «кракозябры».
        with open(filename, "w+", encoding="utf-8") as file:
            # Каждый элемент списка — отдельная строка отчёта.
            file.write("\n".join(lines) + "\n")
        print(f"Информация о погоде записана в файл {filename}")
    except IOError as error:
        # Например, нет прав на запись или диск переполнен.
        print(f"Ошибка при записи в файл: {error}")


def print_summary(payload, unit):
    """Выводит краткую сводку о погоде в консоль."""
    # Здесь поля берём напрямую — к этому моменту
    # api_error_message() уже подтвердил, что ответ корректный.
    print(f"Город                  : {payload['name']}, {payload['sys']['country']}")
    print(
        "Текущая температура    : "
        + kelvin_to_unit(payload["main"]["temp"], unit)
    )
    print(f"Описание погоды        : {payload['weather'][0]['description']}")
    print(f"Влажность              : {payload['main']['humidity']} %")
    print(f"Скорость ветра         : {payload['wind']['speed']} км/ч")
    print(
        "Направление ветра      : "
        + degrees_to_compass(payload["wind"]["deg"])
    )
    print(
        "Время восхода сегодня  : "
        + epoch_to_readable_time(
            payload["sys"]["sunrise"], payload["timezone"]
        )
    )
    print(
        "Время заката сегодня   : "
        + epoch_to_readable_time(
            payload["sys"]["sunset"], payload["timezone"]
        )
    )


def show_instructions():
    """Печатает краткую справку по получению API-ключа."""
    print("Добро пожаловать в приложение «Информация о погоде»!")
    print("API-ключ можно бесплатно получить здесь:")
    print("  https://home.openweathermap.org/users/sign_up")
    print()


def main():
    # Показываем справку со ссылкой на регистрацию.
    show_instructions()

    # .strip() убирает случайные пробелы, которые легко
    # скопировать вместе с ключом или названием города.
    api_key = input("Введите ваш API-ключ OpenWeatherMap: ").strip()

    city = input(
        "Введите город в формате 'Город,CC':\n"
        "  CC — двухбуквенный код страны по ISO 3166-1 alpha-2\n"
        "  (RU — Россия, US — США, GB — Великобритания, DE — Германия и т.д.).\n"
        "  Примеры: 'Moscow,RU', 'London,GB', 'New York,US'.\n"
        "Город: "
    ).strip()

    # Единица измерения: пустой ввод = Цельсий по умолчанию.
    unit_input = input(
        "Единица температуры — 'C' (Цельсий, по умолчанию) "
        "или 'F' (Фаренгейт), Enter — Цельсий: "
    ).strip()
    unit = unit_input.upper() if unit_input else "C"

    # Некорректный ввод не прерывает работу — откатываемся на Цельсий.
    if unit not in ("C", "F"):
        print("Единица температуры должна быть 'C' или 'F'. "
              "Использую 'C' по умолчанию.")
        unit = "C"

    # Запрос к API. Возвращает словарь или None при сетевой ошибке.
    payload = request_weather(api_key, city)
    if not payload:
        print("Не удалось получить данные о погоде. "
              "Проверьте ввод и попробуйте снова.")
        return

    # Проверяем коды ошибок API (неверный ключ, город не найден).
    error = api_error_message(payload)
    if error:
        print(error)
        return

    # Собираем отчёт в виде списка строк — так проще и записать в файл,
    # и при желании распечатать в другом виде.
    report = format_report(payload, unit)

    # Сначала сохраняем в файл, потом печатаем в консоль:
    # если пользователь запустит скрипт в фоне, файл всё равно останется.
    save_report(report)

    print()  # пустая строка для читаемости между блоками вывода
    print_summary(payload, unit)


# Точка входа: main() вызовется, только если запустить файл напрямую,
# а не импортировать его как модуль.
if __name__ == "__main__":
    main()