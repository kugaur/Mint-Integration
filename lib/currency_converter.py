import requests


def rupee_to_dolar(value):
    conversion_rate_url = "http://free.currencyconverterapi.com/api/v5/convert?q=USD_INR&compact=y"
    val = requests.get(conversion_rate_url).json()['USD_INR']['val']
    return value / float(val)