import json
import time
from datetime import datetime

from collectData import collect_data
from bybitFunctions import get_market_price, get_wallet_balance, get_historical_interval


def get_binance_coins():
    while True:
        coin_list = []
        time_multiplication = 1   # TODO Change 1 to 10
        request_time = 'month'   # TODO Change month to today
        result_collect = collect_data(request_time)

        with open('result.json') as file:
            data = json.load(file)

        if data:
            timestamp_from_data = data[0]['timestamp']
            needed_timestamp = (datetime.now().timestamp() - 2629743) * 1000   # TODO Change 2629743 to 600

            if timestamp_from_data > needed_timestamp:
                right_timestamp_boolean = True

            else:
                right_timestamp_boolean = False

        if data and right_timestamp_boolean:

            for index, item in enumerate(data):
                binance_full_title = item.get("full_title")
                binance_full_title = binance_full_title[20:]
                parts = binance_full_title.split(" on ")
                coin_list_string = parts[0].replace(' ', '')
                coin_list = coin_list_string.split(',')

            for index, item in enumerate(coin_list):
                coin_list[index] = coin_list[index] + 'USDT'

            for index, item in enumerate(coin_list):
                print('item: ', item)
                price_of_coin = get_market_price("BTCUSDT")
                print("price_of_coin: ", price_of_coin)
                if price_of_coin != 'error':
                    real_wallet_balance = get_wallet_balance()
                    print('real_wallet_balance: ', real_wallet_balance)
                #
                # if real_wallet_balance != 'error':
                #     get_historical_interval(symbol=item, interval=1, start=1, end=1, limit=1)

            time.sleep(120 * time_multiplication)

        else:
            print('None delist get.')

        time.sleep(3*time_multiplication)


if __name__ == "__main__":
    get_binance_coins()
