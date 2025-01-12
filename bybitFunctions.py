import hashlib
import hmac
import json
import time

import requests

from getEnv import api_key, secret_key


# создание хеша
def hashing(query_string):
    return hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()


# запрос рыночной цены
def get_market_price(symbol, category = 'linear'):
    query_string = "category=" + category + "&symbol=" + symbol
    url = 'https://api.bybit.com/v5/market/tickers?' + query_string
    current_time = int(time.time() * 1000)
    sign = hashing(str(current_time) + api_key + '5000' + query_string)

    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-TIMESTAMP': str(current_time),
        'X-BAPI-SIGN': sign,
        'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.get(url=url, headers=headers)
    data_parsed = json.loads(response.text)

    if data_parsed['result']['list']:
        last_market_price = data_parsed['result']['list'][0]['lastPrice']
        return last_market_price

    else:
        return "error"


def get_wallet_balance(account_type='UNIFIED', coin='USDT'):
    query_string = "accountType=" + account_type + "&coin=" + coin
    url = 'https://api.bybit.com/v5/account/wallet-balance?' + query_string
    current_time = int(time.time() * 1000)
    sign = hashing(str(current_time) + api_key + '5000' + query_string)

    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-TIMESTAMP': str(current_time),
        'X-BAPI-SIGN': sign,
        'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.get(url=url, headers=headers)
    if response != "<Response [401]>":
        data_parsed = json.loads(response.text)
        real_wallet_balance = float(data_parsed['result']['list'][0]['totalEquity']) / 100   # TODO Change 100 to 5
        return real_wallet_balance

    else:
        print("Авторизационный токен протух")
        return "error"


# запрос свечей по интервалу
def get_historical_interval(symbol, interval, start, end, limit, category='linear'):
    query_string = "category=" + category + "&symbol=" + symbol + "&interval=" + interval + "&start=" + str(start) + "&end=" + str(end) + "&limit=" + limit
    url = 'https://api.bybit.com/v5/market/kline?' + query_string
    current_time = int(time.time() * 1000)
    sign = hashing(str(current_time) + api_key + '5000' + query_string)

    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-TIMESTAMP': str(current_time),
        'X-BAPI-SIGN': sign,
        'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.get(url=url, headers=headers)
    data_parsed = json.loads(response.text)
    if data_parsed['retMsg'] == 'OK':
        return data_parsed
    else:
        return "error"


if __name__ == "__main__":
    get_market_price('BTCUSDT')
    get_wallet_balance()
