from binance import Client
from A004_copy.A004_01 import main as A004Main
import yfinance as yf

currency = ['BTC', 'ETH', 'BNB']


client = Client('XzHurmeqBHZRopTs9jPBtYa1IpJopkm12gE4zE6DTMpU7sTPJHE6lDH5cSUvUkCx',
                'rdzqLgixUH7Svt82zb0Hc8ESkwydRA4Sj4pwVW8NazfuNod8zORTxYJoEMRZRUs9')


def APIdata(tickerNum: int):  # DataSet historical[1],
    historicalClose = list(yf.download(
        currency[tickerNum] + '-USD', period='max', interval='1d', progress=False)['Close'])
    historicalClose.reverse()
    return historicalClose


class model:
    TRANSACTIONS_THRESHOLD = 3
    PERCENT_CERTAINTY_THRESHOLD = 1.5

    def check(tickerNum: int):  # check if change is less than threshold then allow // risk management // enough Money? // Order numbers
        HIS = APIdata(tickerNum)
        today_change = ((HIS[0] - HIS[1]) / HIS[1]) * 100
        if abs(today_change) < model.TRANSACTIONS_THRESHOLD:
            return "allow"
        else:
            return "deny"

    def make_order(tickerNum: int):
        allowed_currency = {'ticker': [], 'predict_chg': []}
        PREDICTED = A004Main(tickerNum)['predictedChg']
        if model.check(tickerNum) == "allow" and model.PERCENT_CERTAINTY_THRESHOLD < PREDICTED:
            allowed_currency['ticker'].append(tickerNum)
            allowed_currency['predict_chg'].append(PREDICTED)
        else:
            print(
                currency[tickerNum], "   ---status---:>> denied order :: with predict_chg: ", PREDICTED)


for x in range(3):
    model.make_order(x)

# client.create_test_order(symbol="BTCUSDT", side='BUY',
#                          type='MARKET', quantity= None)
