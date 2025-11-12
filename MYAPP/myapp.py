# # основной модуль программы

from models import Author, User, CurenciesList, CurrencyParser
from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
# эта библиотека нужна для расширения возможностей нашего хоста, то есть теперь у нас есть "/profile" и "/currencies"

import json

main_author = Author('Syrchin Andrey')
main_user = User(1)
currency_parser = CurrencyParser()

available_curr = currency_parser.get_all_available_currencies()

if not available_curr:
    AVAILABLE_CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CHF', 'CAD', 'AUD']
    print("Не удалось загрузить валюты из API, используем стандартный список")

print(f"Доступно валют: {len(available_curr)}")

# По умолчанию выбранные валюты
selected_currencies = ['USD', 'EUR', 'GBP']


def get_currency_data():
    """Получает данные о выбранных валютах"""
    try:
        return currency_parser.get_currencies(selected_currencies)
    except:
        return {}


env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/':
            # Главная страница
            template = env.get_template("index.html")
            result = template.render(
                title='CurrienciesListApp',
                author=main_author.name,
                content=f"Группа: {main_author.group} Автор: {main_author.name}",
                navigation=[
                    {"caption": "Главная", "href": "/"},
                    {"caption": "Профиль", "href": "/profile"},
                    {"caption": "Валюты", "href": "/currencies"}
                ]
            )
        elif parsed_path.path == '/profile':
            # Страница профиля пользователя
            template = env.get_template("profile.html")
            result = template.render(
                title='CurrienciesListApp',
                id=main_user.id,
                content=f"Имя: {main_user.name} ID: {main_user.id}",
                navigation=[
                    {"caption": "Главная", "href": "/"},
                    {"caption": "Профиль", "href": "/profile"},
                    {"caption": "Валюты", "href": "/currencies"}
                ]
            )
        elif parsed_path.path == '/currencies':
            # Страница валют
            template = env.get_template("currencies.html")
            currencies_data = get_currency_data()

            result = template.render(
                title='CurrienciesListApp',
                author=main_author.name,
                currencies=currencies_data.values(),
                available_currencies=available_curr,
                selected_currencies=selected_currencies,
                navigation=[
                    {"caption": "Главная", "href": "/"},
                    {"caption": "Профиль", "href": "/profile"},
                    {"caption": "Валюты", "href": "/currencies"}
                ]
            )
        else:
            # Страница не найдена
            template = env.get_template("index.html")
            result = template.render(
                title='404 - Not Found',
                author=main_author.name,
                content="Страница не найдена",
                navigation=[
                    {"caption": "Главная", "href": "/"},
                    {"caption": "Профиль", "href": "/profile"},
                    {"caption": "Валюты", "href": "/currencies"}
                ]
            )

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(result, "utf-8"))

    def do_POST(self):
        """Обработка выбора валют"""
        global selected_currencies

        if self.path == '/currencies':
            # Получаем данные из формы
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)

            # Обновляем выбранные валюты
            selected_currencies = form_data.get('currencies', [])
            if isinstance(selected_currencies, str):
                selected_currencies = [selected_currencies]

            # Перенаправляем обратно на страницу валют
            self.send_response(303)
            self.send_header('Location', '/currencies')
            self.end_headers()


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('Server is running on http://localhost:8080')
    print('Available routes:')
    print('  http://localhost:8080/ - Главная страница')
    print('  http://localhost:8080/profile - Профиль пользователя')
    print('  http://localhost:8080/currencies - Курсы валют')
    httpd.serve_forever()