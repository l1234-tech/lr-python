from jinja2 import Environment, PackageLoader
from models import Author
from controllers.currencycontroller import CurrencyController
from controllers.usercontroller import UserController


class PagesController:
    def __init__(self, env: Environment):
        self.env = env
        self.currency_ctrl = CurrencyController()
        self.user_ctrl = UserController()
        self.main_author = Author('Сырчин Андрей', 'P3122')

    def render_index(self):
        """Рендеринг главной страницы"""
        template = self.env.get_template("index.html")
        currencies = self.currency_ctrl.get_current_rates()

        valid_currencies = []
        for code, currency in currencies.items():
            if hasattr(currency, 'name') and currency.name:
                valid_currencies.append(currency)

        return template.render(
            title='CurrenciesListApp',
            author=self.main_author,
            group=self.main_author.group,
            currencies=valid_currencies[:10],
            navigation=self._get_navigation()
        )

    def render_user(self, user_id: int):
        """Рендеринг страницы пользователя"""
        template = self.env.get_template("user.html")
        user = self.user_ctrl.get_user(user_id)

        if not user:
            return self._render_error(f"Пользователь с ID {user_id} не найден")

        available_currencies = self.currency_ctrl.get_available_currencies()

        currencies_data = {}
        if user.subscriptions:
            for currency_code in user.subscriptions:
                currency_info = self.currency_ctrl.get_currency_info(currency_code)
                if currency_info:
                    currencies_data[currency_code] = currency_info

        history = {}
        if user.subscriptions:
            for currency_code in user.subscriptions:
                try:
                    hist = self.currency_ctrl.get_currency_history(currency_code, 30)
                    if hist and len(hist) > 0:
                        history[currency_code] = hist
                except Exception as e:
                    print(f"Ошибка получения истории для {currency_code}: {e}")
                    mock_history = self._create_mock_history(currency_code, 30)
                    if mock_history:
                        history[currency_code] = mock_history

        return template.render(
            title=f'Пользователь {user.name}',
            user=user,
            currencies_data=currencies_data,
            available_currencies=available_currencies or [],
            history=history,
            navigation=self._get_navigation()
        )

    def render_currencies(self):
        """Рендеринг страницы валют"""
        template = self.env.get_template("currencies.html")
        currencies = self.currency_ctrl.get_current_rates()

        valid_currencies = []
        for code, currency in currencies.items():
            if hasattr(currency, 'name') and currency.name:
                valid_currencies.append(currency)

        valid_currencies.sort(key=lambda x: x.name_curr)

        available_currencies = self.currency_ctrl.get_available_currencies()
        selected_currencies = self.currency_ctrl.selected_currencies

        return template.render(
            title='Курсы валют',
            currencies=valid_currencies,
            available_currencies=sorted(available_currencies) if available_currencies else [],
            selected_currencies=selected_currencies,
            navigation=self._get_navigation()
        )

    def _create_mock_history(self, currency_code: str, days: int):
        """Создает фиктивную историю для валюты"""
        from datetime import datetime, timedelta
        import random

        history = []
        current_date = datetime.now()

        base_values = {
            'USD': 90.0, 'EUR': 98.0, 'GBP': 115.0, 'JPY': 0.6,
            'CNY': 12.5, 'CHF': 105.0, 'CAD': 65.0, 'AUD': 60.0,
            'KZT': 0.19, 'UAH': 2.3, 'BYN': 28.0, 'AMD': 0.23
        }

        base_value = base_values.get(currency_code, 50.0)

        for i in range(days):
            date_str = (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
            trend = 0.001 * i
            variation = base_value * 0.02 * (random.random() - 0.5)
            value = base_value + trend + variation

            history.append({
                "date": date_str,
                "value": max(value, 0.01)
            })

        return history

    def _render_error(self, message: str):
        """Рендеринг страницы ошибки"""
        template = self.env.get_template("base.html")
        return template.render(
            title='Ошибка',
            author=self.main_author,
            navigation=self._get_navigation(),
            content=f'''
            <div class="container mt-4">
                <div class="alert alert-danger">
                    <h4>Ошибка!</h4>
                    <p>{message}</p>
                </div>
                <a href="/" class="btn btn-primary">На главную</a>
            </div>
            '''
        )

    def render_author(self):
        """Рендеринг страницы об авторе"""
        template = self.env.get_template("author.html")
        return template.render(
            title='Об авторе',
            author=self.main_author,
            navigation=self._get_navigation()
        )

    def render_users(self):
        """Рендеринг страницы пользователей"""
        template = self.env.get_template("users.html")
        users = self.user_ctrl.get_all_users()

        user_data = []
        total_subscriptions = 0
        currency_count = {}

        for user in users:
            user_dict = user.to_dict()
            user_data.append(user_dict)

            user_subscriptions = user.subscriptions
            total_subscriptions += len(user_subscriptions)

            for currency in user_subscriptions:
                currency_count[currency] = currency_count.get(currency, 0) + 1

        avg_subscriptions = total_subscriptions / len(users) if users else 0
        most_popular_currency = max(currency_count.items(), key=lambda x: x[1])[0] if currency_count else "Нет данных"

        return template.render(
            title='Пользователи',
            users=user_data,
            total_subscriptions=total_subscriptions,
            avg_subscriptions=round(avg_subscriptions, 1),
            most_popular_currency=most_popular_currency,
            navigation=self._get_navigation()
        )

    def render_report1(self):
        """Рендеринг отчета 1"""
        template = self.env.get_template("report.html")
        return template.render(
            title='Отчет 1 - Описание проекта',
            author=self.main_author,
            navigation=self._get_navigation()
        )

    def render_report2(self):
        """Рендеринг отчета 2"""
        template = self.env.get_template("report2.html")
        return template.render(
            title='Отчет 2 - Реализация и тестирование',
            author=self.main_author,
            navigation=self._get_navigation()
        )

    def render_404(self):
        """Рендеринг страницы 404"""
        return self._render_error("Страница не найдена")

    def _get_navigation(self):
        """Получить навигационное меню"""
        return [
            {"caption": "Главная", "href": "/"},
            {"caption": "Об авторе", "href": "/author"},
            {"caption": "Пользователи", "href": "/users"},
            {"caption": "Валюты", "href": "/currencies"},
            {"caption": "Отчет 1", "href": "/report"},
            {"caption": "Отчет 2", "href": "/report2"}
        ]
