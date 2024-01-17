class CurrencyConverterViewModel:
    def __init__(self, currency_data):
        self.currency_data = currency_data

    def get_currency_rate(self, char_code):
        """ Возвращает курс и номинал для заданной валюты по ее символьному коду. """
        for currency in self.currency_data:
            if currency['CharCode'] == char_code:
                return currency['Value'], currency['Nominal']
        return None, None
        
    def convert_currency(self, amount, from_currency, to_currency):
        """ Конвертирует сумму из одной валюты в другую. """
        from_rate, from_nominal = self.get_currency_rate(from_currency)
        to_rate, to_nominal = self.get_currency_rate(to_currency)

        if from_rate and to_rate:
        # Переводим сумму в базовую валюту
            amount_in_base = (amount * from_rate) / from_nominal
        # Переводим сумму из базовой валюты в целевую валюту
            return (amount_in_base * to_nominal) / to_rate
        return None
