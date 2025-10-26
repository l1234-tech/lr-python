import requests
import sys
import io
import functools


def trace(func=None, *, handle=sys.stdout):
    print(f"decorated func: {func}, {handle}")
    if func is None:
        print('func is None')
        return lambda func: trace(func, handle=handle)
    else:
        print(f'{func.__name__}, {handle}')

    @functools.wraps(func)
    def inner(*args, **kwargs):
        handle.write(f"Using handling output\n")
        # print(func.__name__, args, kwargs)
        return func(*args, **kwargs)

    # print('return inner')
    return inner

notstandartstream = io.StringIO()
@trace
def get_currencies(currency_codes:list , url:str = 'https://www.cbr-xml-daily.ru/daily_json.js' , handle = notstandartstream) -> dict:
    """

    {"GBP" : 127.4962 , "EUR" : 106,1028}
    """
    try:
        print (handle)
        # print(r.status_code)
        response = requests.get(url)

        response.raise_for_status()
        data = response.json()

        currencies = {}

        # print(data)
        if "Valute" in data:
            for code in currency_codes:
                if code in data["Valute"]:
                    currencies[code] = data["Valute"][code]["Value"]
                else:
                    currencies[code] = f"Код валюты '{code}' не найден."
        return currencies

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе API: {e}" , file = handle)
        handle.write(f"Ошибка при запросе API: {e}")
        raise requests.exceptions.RequestException('Упали с исключением')
        # специально понимаем ошибку, чтобы понять что не так
        # return None

if __name__ == '__main__':
    currency_list = ['USD', 'EUR', 'GBP' , 'JPY']
    currency_data = get_currencies(currency_list)
    res = get_currencies(currency_list)

    print(res)
