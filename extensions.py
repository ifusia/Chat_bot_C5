import requests
import json
from config import keys, ACCESS_KEY


class ConversionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionException(f'Cannot convert same values {base}')

        quote_ticker, base_ticker = keys[quote], keys[base]

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'I need a number to convert, not a {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/{ACCESS_KEY}/pair/{quote_ticker}/{base_ticker}/{amount}')
        if r.status_code != 200:
            raise ConversionException('Error during a request response')

        result = json.loads(r.content)
        if result["result"] != "success":
            raise ConversionException('Error during a request response')

        total_base = result["conversion_result"]

        return total_base