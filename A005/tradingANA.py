import pandas as pd
from binance import Client
from A004_copy.A004_01 import main as A004Main
import yfinance as yf
import time

currency = ['BTC', 'ETH', 'BNB']


client = Client('XzHurmeqBHZRopTs9jPBtYa1IpJopkm12gE4zE6DTMpU7sTPJHE6lDH5cSUvUkCx',
                'rdzqLgixUH7Svt82zb0Hc8ESkwydRA4Sj4pwVW8NazfuNod8zORTxYJoEMRZRUs9')


def APIdata(tickerNum: int):  # DataSet historical[1],
    historicalClose = list(yf.download(
        currency[tickerNum] + '-USD', period='max', interval='1d', progress=False)['Close'])
    historicalClose.reverse()
    return historicalClose


class transaction:
    A_SHARE = 100
    DECI = [5, 4, 3]

    def buy(tickerNum: int, predicted: float):
        price = client.get_symbol_ticker(symbol=currency[tickerNum] + 'USDT')
        # PREDICTED_PRICE = round(
        #     A004Main(tickerNum)['predictedPrice'], transaction.DECI[tickerNum])
        predictPrice = float(round(float(
            price['price']) + (float(price['price']) * predicted / 100), 2))
        currency_quantity = round(
            transaction.A_SHARE / float(price['price']), transaction.DECI[tickerNum])

        client.create_test_order(
            symbol=currency[tickerNum] + 'USDT', side='BUY', type='MARKET', quantity=currency_quantity)
        time.sleep(3)
        client.create_test_order(
            symbol=currency[tickerNum] + 'USDT', side='SELL', timeInForce='GTC', type='LIMIT', quantity=currency_quantity, price=predictPrice)
        transaction.save_transaction(
            tickerNum, price, predictPrice, predicted,  currency_quantity, side='BUY')

    def save_transaction(tickerNum: int, price: float, predicted_sellAt: any, predict_percent: float, amountINcurrency: float, side: str):
        import pickle
        import json
        from datetime import datetime
        transaction_dict = {'period': datetime.now().strftime(
            '%m/%d/%Y, %H:%M:%S'), 'currency': currency[tickerNum], 'price': price['price'], 'side': side, 'sellAt': predicted_sellAt, 'sellAt_%': predict_percent, 'amount': amountINcurrency}

        import sqlite3
        con = sqlite3.connect('transaction.db')
        cur = con.cursor()
        cur.execute("insert into buy values (?, ?, ?, ?, ? ,?, ?)", (transaction_dict['period'], transaction_dict['currency'], transaction_dict[
                    'price'], transaction_dict['side'], transaction_dict['sellAt'], transaction_dict['sellAt_%'], transaction_dict['amount']))
        con.commit()
        con.close()

        # save open order file
        try:
            with open('data.json') as json_file:
                output = json.load(json_file)
            output['open'] = int(output['open'])+1
            a_file = open("data.json", "w")
            json.dump(output, a_file)
            a_file.close()
        except:
            dict = {'open': 0}
            a_file = open("data.json", "w")
            json.dump(dict, a_file)
            a_file.close()


class model:
    TRANSACTIONS_THRESHOLD = 5  # percent change not higher than TRANSACTIONS_THRESHOLD
    PERCENT_CERTAINTY_THRESHOLD = 1.5  # higher than predicted percentage

    def check(tickerNum: int):  # check if change is less than threshold then allow // risk management // enough Money? // Order numbers
        HIS = APIdata(tickerNum)
        today_change = float(((HIS[0] - HIS[1]) / HIS[1]) * 100)
        if (abs(today_change) < model.TRANSACTIONS_THRESHOLD) and (len(client.get_open_orders()) == 0):
            return "allow"
        else:
            return "deny", today_change

    def make_order():
        allowed_currency = {}
        for x in range(len(currency)):
            PREDICTED = A004Main(x)['predictedChg']
            if model.check(x) == "allow" and model.PERCENT_CERTAINTY_THRESHOLD < PREDICTED:
                allowed_currency.update({x: PREDICTED})
            else:
                print(
                    currency[x], "   ---status---:>> denied order :: with predict_chg: ", PREDICTED, model.check(x)[1])

        sorted_dict = {}
        sorted_keys = sorted(
            allowed_currency, key=allowed_currency.get)  # [1, 3, 2]
        for w in sorted_keys:
            sorted_dict[w] = allowed_currency[w]
        allowed_currency = sorted_dict
        buy_ticker_num = int(
            allowed_currency[list(allowed_currency.keys())[-1]])
        transaction.buy(buy_ticker_num, predicted=A004Main(
            buy_ticker_num)['predictedChg'])


model.make_order()
