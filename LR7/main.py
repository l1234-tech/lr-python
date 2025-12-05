import requests
import sys
import io
import functools
import logging

def logger(func = None, *, handle = sys.stdout):
    """
    Декоратор для логирования вызовов функций и их результатов.
    Параметры:
    func : декорируемая функция. Если None, возвращает частично применённый декоратор.
    handle : ключевой параметр
    Объект для логирования может быть:
    - logging.Logger: логирование через методы info(), error()
    - Объект с методом write() (sys.stdout, io.StringIO)
    По умолчанию sys.stdout.
    Возвращает: callable
    Декорированная функция с логированием.
    """

    if func is None:
        return lambda f: logger(f, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        func_name = func.__name__

        try:
            result = func(*args, **kwargs)

            success_message = f"Логгер отработал успешно '{func_name}'"

            if isinstance(handle, logging.Logger):
                handle.info(success_message)
            else:
                handle.write(f"INFO: {success_message}\n")

            return result

        except Exception as e:
            error_message = f"Ошибка в '{func_name}': {type(e).__name__}: {str(e)}"

            if isinstance(handle, logging.Logger):
                handle.error(error_message)
            else:
                handle.write(f"ERROR: {error_message}\n")
            raise

    return inner


@logger(handle=sys.stdout)
def get_currencies(currency_codes,
                   url: str = 'https://www.cbr-xml-daily.ru/daily_json.js'):
    """
    Получает текущие курсы валют с API Центрального Банка России.

    Параметры:
    currency_codes: список кодов валют (например, ['USD', 'EUR', 'GBP']).
    url: URL API Центрального Банка.

    Возвращает:
        Словарь, где ключи - коды валют, значения - курсы валют к рублю.

    Исключения:
    ConnectionError - если API недоступен или произошла ошибка сети.
    ValueError - если полученные данные не являются корректным JSON.
    KeyError - если в ответе API отсутствует ключ 'Valute' или валюта.
    TypeError - если курс валюты имеет неверный тип.
    """

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка подключения к API: {str(e)}") from e

    try:
        data = response.json()
    except ValueError as e:
        raise ValueError(f"Ошибка парсинга JSON: {str(e)}") from e

    if "Valute" not in data:
        raise KeyError("В ответе API отсутствует ключ 'Valute'")

    currencies = {}

    for code in currency_codes:
        if code not in data["Valute"]:
            raise KeyError(f"Валюта с кодом '{code}' отсутствует в данных API")

        currency_data = data["Valute"][code]

        if not isinstance(currency_data.get("Value"), (int, float)):
            raise TypeError(f"Курс валюты '{code}' имеет неверный тип: {type(currency_data.get('Value'))}")

        currencies[code] = currency_data["Value"]

    return currencies

@logger(handle=sys.stdout)
def solve_quadratic(a: float, b: float, c: float):
    """
    Решает квадратное уравнение вида: ax² + bx + c = 0
    Параметры:
    a, b, c - коэффициенты уравнения
    Возвращает:
    - None: если нет действительных корней
    - float: один корень
    - tuple: два корня
    Исключения:
    TypeError, ValueError - при некорректных входных данных
    """

    if not all(isinstance(coef, (int, float)) for coef in [a, b, c]):
        raise TypeError("Все коэффициенты должны быть числами")

    if a == 0:
        if b == 0:
            if c == 0:
                return None
            else:
                raise ValueError("Уравнение не имеет решений")
        return -c / b

    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        return None
    elif discriminant == 0:
        return -b / (2 * a)
    else:
        sqrt_d = discriminant ** 0.5
        root1 = (-b + sqrt_d) / (2 * a)
        root2 = (-b - sqrt_d) / (2 * a)
        return root1, root2


def setup_file_logger():
    """Настраивает и возвращает логгер для записи в файл."""
    file_logger = logging.getLogger("currency_file")
    file_logger.setLevel(logging.INFO)

    file_logger.handlers = []

    file_handler = logging.FileHandler('currency.log', mode='w', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    file_logger.addHandler(file_handler)
    return file_logger


if __name__ == '__main__':
    print("\nПолучение курсов валют:")
    try:
        currency_data = get_currencies(['USD', 'EUR'])
        print(f"Результат: {currency_data}")
    except Exception as e:
        print(f"Ошибка: {e}")

    print("\nРешение квадратных уравнений:")

    test_tuple = [
        (1, -3, 2, "x**2 - 3x + 2 = 0"),
        (1, 2, 1, "x**2 + 2x + 1 = 0"),
        (1, 0, 1, "x**2 + 1 = 0"),
    ]

    for a, b, c, desc in test_tuple:
        print(f"{desc}")
        try:
            result = solve_quadratic(a, b, c)
            print(f"Корни: {result}")
        except Exception as e:
            print(f"Ошибка: {e}")

    print("\nЛогирование в файл:")
    try:
        file_logger = setup_file_logger()

        @logger(handle=file_logger)
        def get_usd_rate():
            return get_currencies(['USD'])

        result = get_usd_rate()
        print(f"Курс USD записан в currency.log: {result}")
    except Exception as e:
        print(f"Ошибка: {e}")

    print("\nЛогирование в StringIO:")
    string_stream = io.StringIO()

    @logger(handle=string_stream)
    def multiply(x: int, y: int) -> int:
        return x * y

    result = multiply(5, 7)
    print(f"Результат: {result}")
    print(f"Логи: {string_stream.getvalue().strip()}")
