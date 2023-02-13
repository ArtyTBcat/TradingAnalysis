import numpy as np
import logging
from binance import Client
from A004_copy.A004_01 import main as A004Main
import yfinance as yf
import time
from datetime import datetime

currency = ['BTC', 'BNB', 'ETH', 'ADA', 'XRP',
            'SOL', 'TRX', 'VET', 'FTM', 'DOT', 'LTC', 'ATOM']

logging.basicConfig(filename='log.log',
                    encoding='utf-8', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)

client = Client('XzHurmeqBHZRopTs9jPBtYa1IpJopkm12gE4zE6DTMpU7sTPJHE6lDH5cSUvUkCx',
                'rdzqLgixUH7Svt82zb0Hc8ESkwydRA4Sj4pwVW8NazfuNod8zORTxYJoEMRZRUs9')


def APIdata(tickerNum: int):  # DataSet historical[1],
    historicalClose = list(yf.download(
        currency[tickerNum] + '-USD', period='max', interval='1d', progress=False)['Close'])
    historicalClose.reverse()
    return historicalClose


def error():
    import sys
    import traceback
    error_msg = sys.exc_info()
    traceback.print_exc()
    # print('error: ', error_msg)
    logging.error(error_msg)
    COUNT_DOWN = 60  # sec
    for x in range(COUNT_DOWN):
        time.sleep(1)
        print("waiting for cool down ERROR T -",
              COUNT_DOWN-x, " seconds", end='\r')


class transaction:
    A_SHARE = 200  # A Transaction share USDT
    DECI = [5, 3, 4, 1, 0, 2, 1, 1, 0, 2, 3, 2]

    def buy(tickerNum: int, predicted: float):
        logging.debug("Making transaction")
        price = client.get_symbol_ticker(symbol=currency[tickerNum] + 'USDT')
        # PREDICTED_PRICE = round(
        #     A004Main(tickerNum)['predictedPrice'], transaction.DECI[tickerNum])
        predictPrice = float(round(float(
            price['price']) + (float(price['price']) * predicted / 100), 2))
        currency_quantity = round(
            transaction.A_SHARE / float(price['price']), transaction.DECI[tickerNum])
        client.create_order(
            symbol=currency[tickerNum] + 'USDT', side='BUY', type='MARKET', quantity=currency_quantity)
        time.sleep(3)
        client.create_order(
            symbol=currency[tickerNum] + 'USDT', side='SELL', timeInForce='GTC', type='LIMIT', quantity=currency_quantity, price=predictPrice)
        transaction.save_transaction(
            tickerNum, price, predictPrice, predicted,  currency_quantity, side='BUY')

    def save_transaction(tickerNum: int, price: float, predicted_sellAt: any, predict_percent: float, amountINcurrency: float, side: str):
        import json
        transaction_dict = {'period': datetime.now().strftime(
            '%m/%d/%Y %H:%M:%S'), 'currency': currency[tickerNum], 'price': price['price'], 'side': side, 'sellAt': predicted_sellAt, 'sellAt_%': predict_percent, 'amount': amountINcurrency}
        logging.warning('Done Transaction: ' + str(transaction_dict))
        print(transaction_dict)
        import sqlite3
        con = sqlite3.connect('transaction.db')
        cur = con.cursor()
        cur.execute("insert into buy values (?, ?, ?, ?, ? ,?, ?)", (transaction_dict['period'], transaction_dict['currency'], transaction_dict[
                    'price'], transaction_dict['side'], transaction_dict['sellAt'], transaction_dict['sellAt_%'], transaction_dict['amount']))
        gain = (float(transaction_dict['sellAt']) * float(transaction_dict['amount'])
                ) - (float(transaction_dict['price']) * float(transaction_dict['amount']))
        cur.execute("insert into balance values (?, ?, ?)",
                    (transaction_dict['period'], transaction_dict['currency'], gain))
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
        logging.debug('Done saving transaction')


class model:
    TRANSACTIONS_THRESHOLD = 5  # percent change not higher than TRANSACTIONS_THRESHOLD
    PERCENT_CERTAINTY_THRESHOLD = 1.3  # higher than predicted percentage

    def volatility(tickerNum: int):
        listChg = []
        abs_listChg = []
        historical = APIdata(tickerNum)
        for count in range(len(historical)):
            try:
                percentChg = (
                    (historical[count] - historical[count+1]) / historical[count+1]) * 100
                listChg.append(percentChg)
                abs_listChg.append(percentChg)
            except:
                pass
        vol = np.average(abs_listChg)
        return vol

    # check if change is less than threshold then allow // risk management // enough Money? // Order numbers
    def check(tickerNum: int, openOrder: list):
        logging.debug('Checking Parameters: ' + str(currency[tickerNum]))
        HIS = APIdata(tickerNum)
        today_change = float(((HIS[0] - HIS[2]) / HIS[2]) * 100)
        if (abs(today_change) < model.TRANSACTIONS_THRESHOLD) and (len(openOrder) == 0):
            return "allow", today_change
        else:
            return "deny", today_change

    def make_order():
        allowed_currency = {}
        OPEN_ORDER = client.get_open_orders()
        for x in range(len(currency)):
            VOLATILITY = model.volatility(x)
            # PREDICTED = A004Main(x)['predictedChg'] - VOLATILITY
            PREDICTED = A004Main(x)['predictedChg']
            logging.info(str(currency[x]) + " predict_chg: " + str(PREDICTED) + " volatility: " + str(VOLATILITY) +
                         "  today_chg: " + str(model.check(x, OPEN_ORDER)[1]))

            if model.check(x, OPEN_ORDER)[0] == "allow" and model.PERCENT_CERTAINTY_THRESHOLD < PREDICTED:
                allowed_currency.update({x: PREDICTED})
                logging.info(str(currency[x]) + " ACCEPTED: signal for order")
            else:
                print(
                    currency[x], "   ---INFO---:>> denied order :: with predict_chg: ", PREDICTED, VOLATILITY,  model.check(x, OPEN_ORDER)[1])

        if allowed_currency:
            sorted_dict = {}
            sorted_keys = sorted(
                allowed_currency, key=allowed_currency.get)  # [1, 3, 2]
            for w in sorted_keys:
                sorted_dict[w] = allowed_currency[w]
            allowed_currency = sorted_dict
            buy_ticker_num = list(allowed_currency.keys())[-1]
            PREDICTED_PRICE = allowed_currency[buy_ticker_num]
            transaction.buy(buy_ticker_num, predicted=PREDICTED_PRICE)


# model.make_order()
TIME_COUNT = 60
while True:
    try:
        model.make_order()
        for x in range(TIME_COUNT):
            time.sleep(60)
            print(datetime.now().strftime('%m/%d/%Y %H:%M:%S'),
                  "pending ", x, " min", end="\r")
        print("\n")
    except:
        error()
