from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, PackageLoader, select_autoescape
import sqlite3
from controllers.pages import PagesController

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

pages_ctrl = PagesController(env)

class CurrencyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        try:
            if parsed_path.path == '/':
                html_content = pages_ctrl.render_index()

            elif parsed_path.path == '/author':
                html_content = pages_ctrl.render_author()

            elif parsed_path.path == '/users':
                html_content = pages_ctrl.render_users()

            elif parsed_path.path == '/user':
                if 'id' in query_params:
                    try:
                        user_id = int(query_params['id'][0])
                        html_content = pages_ctrl.render_user(user_id)
                    except ValueError:
                        html_content = self._render_error("Неверный ID пользователя")
                else:
                    html_content = self._render_error("ID пользователя не указан")

            elif parsed_path.path == '/currencies':
                html_content = pages_ctrl.render_currencies()

            elif parsed_path.path == '/report':
                html_content = pages_ctrl.render_report1()

            elif parsed_path.path == '/report2':
                html_content = pages_ctrl.render_report2()

            elif parsed_path.path == '/debug':
                html_content = self._render_debug_page()

            else:
                html_content = pages_ctrl.render_404()

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

        except Exception as e:
            print(f"Ошибка обработки запроса: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            error_html = f"""
            <html><body>
            <h1>500 - Внутренняя ошибка сервера</h1>
            <p>{str(e)}</p>
            <a href="/">На главную</a>
            </body></html>
            """
            self.wfile.write(error_html.encode('utf-8'))

    def do_POST(self):
        parsed_path = urlparse(self.path)

        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)
        except:
            form_data = {}

        from controllers.usercontroller import UserController
        from controllers.currencycontroller import CurrencyController

        user_ctrl = UserController()
        currency_ctrl = CurrencyController()

        if parsed_path.path == '/users/add':
            if 'name' in form_data and form_data['name'][0]:
                name = form_data['name'][0].strip()
                if name:
                    user_ctrl.add_user(name)
                    self._redirect('/users')
                else:
                    self._redirect('/users?error=empty_name')
            else:
                self._redirect('/users?error=no_name')

        elif parsed_path.path == '/user/subscription':
            if all(key in form_data for key in ['user_id', 'currency_code', 'action']):
                try:
                    user_id = int(form_data['user_id'][0])
                    currency_code = form_data['currency_code'][0].upper().strip()
                    action = form_data['action'][0]

                    if not currency_code:
                        self._redirect(f'/user?id={user_id}&error=empty_currency')
                        return

                    subscribe = (action == 'subscribe')
                    success = user_ctrl.update_user_subscription(user_id, currency_code, subscribe)

                    if success:
                        self._redirect(f'/user?id={user_id}')
                    else:
                        self._redirect(f'/user?id={user_id}&error=subscription_failed')

                except Exception as e:
                    print(f"Ошибка обновления подписки: {e}")
                    self._redirect(f'/user?id={form_data.get("user_id", [""])[0]}&error=server_error')
            else:
                if 'user_id' in form_data:
                    user_id = form_data['user_id'][0]
                    self._redirect(f'/user?id={user_id}&error=no_currency_selected')
                else:
                    self._redirect('/users')

        elif parsed_path.path == '/currencies/add':
            if 'currency_code' in form_data:
                currency_code = form_data['currency_code'][0].upper()
                success = currency_ctrl.add_currency(currency_code)
                self._redirect('/currencies')

        elif parsed_path.path == '/currencies/remove':
            if 'currency_code' in form_data:
                currency_code = form_data['currency_code'][0].upper()
                success = currency_ctrl.remove_currency(currency_code)
                self._redirect('/currencies')

        elif parsed_path.path == '/currencies/select':
            if 'currencies' in form_data:
                selected = form_data['currencies']
                if isinstance(selected, str):
                    selected = [selected]
                selected = [code.upper() for code in selected if code]
                currency_ctrl.update_selected_currencies(selected)
                self._redirect('/currencies')
            else:
                currency_ctrl.update_selected_currencies([])
                self._redirect('/currencies')

        elif parsed_path.path == '/currencies/update':
            currency_ctrl.refresh_currencies()
            self._redirect('/currencies')

        else:
            self.send_response(404)
            self.end_headers()

    def _redirect(self, location: str):
        self.send_response(303)
        self.send_header('Location', location)
        self.end_headers()

    def _render_error(self, message: str):
        template = env.get_template("base.html")
        return template.render(
            title='Ошибка',
            author=pages_ctrl.main_author,
            navigation=pages_ctrl._get_navigation(),
            content=f'<div class="alert alert-danger">{message}</div>'
        )

    def _render_debug_page(self):
        conn = sqlite3.connect('currencies.db')
        cursor = conn.cursor()

        debug_info = "<h3>Отладочная информация</h3>"

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        debug_info += f"<h4>Пользователи ({len(users)}):</h4><ul>"
        for user in users:
            debug_info += f"<li>ID: {user[0]}, Имя: {user[1]}</li>"
        debug_info += "</ul>"

        cursor.execute("SELECT * FROM user_subscriptions")
        subscriptions = cursor.fetchall()
        debug_info += f"<h4>Подписки ({len(subscriptions)}):</h4><ul>"
        for sub in subscriptions:
            debug_info += f"<li>Пользователь {sub[0]} -> {sub[1]}</li>"
        debug_info += "</ul>"

        conn.close()

        template = env.get_template("base.html")
        return template.render(
            title='Отладка',
            author=pages_ctrl.main_author,
            navigation=pages_ctrl._get_navigation(),
            content=debug_info
        )

    def log_message(self, format, *args):
        print(f"{self.client_address[0]} - {self.command} {self.path}")

    def test_subscriptions(self):
        conn = sqlite3.connect('currencies.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("Таблицы в базе:", tables)

        cursor.execute("SELECT * FROM user_subscriptions")
        subscriptions = cursor.fetchall()
        print("Подписки в базе:", subscriptions)

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print("Пользователи в базе:", users)

        conn.close()


def main():
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, CurrencyHTTPRequestHandler)

    print("=" * 60)
    print("CurrenciesListApp запущен!")
    print("=" * 60)
    print(f"Сервер доступен по адресу: http://{server_address[0]}:{server_address[1]}")
    print("=" * 60)
    print("Доступные маршруты:")
    print("  /              - Главная страница")
    print("  /author        - Об авторе")
    print("  /users         - Список пользователей")
    print("  /user?id=...   - Профиль пользователя")
    print("  /currencies    - Курсы валют")
    print("  /report        - Отчет 1")
    print("  /report2       - Отчет 2")
    print("  /debug         - Отладочная информация")

    try:
        handler = CurrencyHTTPRequestHandler
        handler_instance = handler(None, None, None)
        handler_instance.test_subscriptions()
    except:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
        httpd.server_close()


if __name__ == '__main__':
    main()
