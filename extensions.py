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

        if quote == base:
            raise ConversionException(f'Cannot convert same values {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Cannot find a {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Cannot find a {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'I need a number to convert, not a {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/{ACCESS_KEY}/pair/{base_ticker}/{quote_ticker}/{amount}')

        total_base = json.loads(r.content)[keys[base]]

        return total_base
