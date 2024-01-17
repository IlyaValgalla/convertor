from datetime import datetime
from currency_api import get_currency_rates
from currency_converter_view import CurrencyConverterView
from currency_converter_viewmodel import CurrencyConverterViewModel

def main():
    # Получаем текущую дату
    date = datetime.today()

    # Получаем данные о курсах валют на текущую дату
    currency_rates = get_currency_rates(date)
    if currency_rates:
        # Инициализация ViewModel с полученными данными
        vm = CurrencyConverterViewModel(currency_rates)

        # Получаем список кодов валют для использования в GUI
        currency_codes = [currency['CharCode'] for currency in currency_rates]

        # Создание и запуск GUI
        app = CurrencyConverterView(vm, currency_codes)
        app.mainloop()
    else:
        print("Не удалось получить данные о курсах валют.")

if __name__ == "__main__":
    main()
