import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def get_currency_rates(date):
    # Формируем URL для запроса с заданной датой
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date.strftime('%d/%m/%Y')}"

    # Делаем запрос к API
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем на ошибки запроса

        # Парсинг XML-ответа
        root = ET.fromstring(response.content)
        currency_data = []

        for valute in root.findall('Valute'):
            currency_info = {
                'ID': valute.get('ID'),
                'NumCode': valute.find('NumCode').text,
                'CharCode': valute.find('CharCode').text,
                'Nominal': int(valute.find('Nominal').text),
                'Name': valute.find('Name').text,
                'Value': float(valute.find('Value').text.replace(',', '.'))
            }
            currency_data.append(currency_info)

        return currency_data

    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None
