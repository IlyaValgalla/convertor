import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from currency_converter_viewmodel import CurrencyConverterViewModel
from currency_api import get_currency_rates
from datetime import datetime

class CurrencyConverterView(tk.Tk):
    def __init__(self, view_model, currency_codes):
        super().__init__()
        self.title("Конвертер валют")
        self.geometry("400x300")
        self.configure(bg='lightblue')

        # Настройка стилей
        self.style = ttk.Style()
        self.style.configure('TLabel', background='lightblue', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), background='lightgreen')
        self.style.configure('TEntry', font=('Arial', 10), background='white')
        self.style.configure('TCombobox', font=('Arial', 10))

        self.view_model = view_model
        self.currency_codes = currency_codes
        self.create_widgets()
        self.update_currency_rates()

    def create_widgets(self):
        # Выбор даты
        self.date_label = ttk.Label(self, text="Выберите дату:", style='TLabel')
        self.date_label.grid(column=0, row=0, padx=10, pady=10)

        self.calendar = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.calendar.grid(column=1, row=0, padx=10, pady=10)
        self.calendar.bind("<<DateEntrySelected>>", self.on_date_change)

        # Выбор валют
        self.from_currency_label = ttk.Label(self, text="Из:", style='TLabel')
        self.from_currency_label.grid(column=0, row=1, padx=10, pady=10)

        self.from_currency_combo = ttk.Combobox(self, style='TCombobox')
        self.from_currency_combo.grid(column=1, row=1, padx=10, pady=10)

        self.to_currency_label = ttk.Label(self, text="В:", style='TLabel')
        self.to_currency_label.grid(column=0, row=2, padx=10, pady=10)

        self.to_currency_combo = ttk.Combobox(self, style='TCombobox')
        self.to_currency_combo.grid(column=1, row=2, padx=10, pady=10)

        # Ввод суммы для конвертации
        self.amount_label = ttk.Label(self, text="Введите сумму:", style='TLabel')
        self.amount_label.grid(column=0, row=3, padx=10, pady=10)

        self.amount_entry = ttk.Entry(self, style='TEntry')
        self.amount_entry.grid(column=1, row=3, padx=10, pady=10)

        # Кнопка конвертации
        self.convert_button = ttk.Button(self, text="Конвертировать", command=self.convert, style='TButton')
        self.convert_button.grid(column=1, row=4, padx=10, pady=10)

        # Отображение результата
        self.result_label = ttk.Label(self, text="Результат:", style='TLabel')
        self.result_label.grid(column=0, row=5, padx=10, pady=10)

        self.result = tk.StringVar()
        self.result_display = ttk.Label(self, textvariable=self.result, style='TLabel')
        self.result_display.grid(column=1, row=5, padx=10, pady=10)

    def on_date_change(self, event):
        self.update_currency_rates()

    def update_currency_rates(self):
        selected_date = self.calendar.get_date()
        currency_rates = get_currency_rates(selected_date)
        if currency_rates:
            self.view_model.currency_data = currency_rates
            self.currency_codes = [f"{currency['CharCode']} - {currency['Name']}" for currency in currency_rates]
            self.from_currency_combo['values'] = self.currency_codes
            self.to_currency_combo['values'] = self.currency_codes
            self.from_currency_combo.current(0)
            self.to_currency_combo.current(1)
        else:
            print("Не удалось получить данные о курсах валют.")

    def convert(self):
        try:
            from_currency = self.from_currency_combo.get().split(" - ")[0]
            to_currency = self.to_currency_combo.get().split(" - ")[0]
            amount = float(self.amount_entry.get())
            result = self.view_model.convert_currency(amount, from_currency, to_currency)
            self.result.set(f"{result:.2f}")
        except ValueError:
            self.result.set("Некорректная сумма")
        except Exception as e:
            self.result.set("Ошибка конвертации")

# Пример использования
if __name__ == "__main__":
    vm = CurrencyConverterViewModel(None)
    app = CurrencyConverterView(vm)
    app.mainloop()
