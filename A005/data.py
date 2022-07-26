import yfinance as yf
import numpy as np
import pandas as pd

currency = ['BTC', 'ETH', 'BNB']


def APIdata(tickerNum: int):  # DataSet historical[1],
    historicalClose = list(yf.download(
        currency[tickerNum] + '-USD', period='max', interval='1d', progress=False)['Close'])
    historicalClose.reverse()
    return historicalClose


class models:
    def percentChange(tickerNum: int):
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
        return listChg, abs_listChg

    def volatility(tickerNum: int):
        vol = np.average(models.percentChange(tickerNum)[1])
        print(vol)


class collections:
    def volatility(tickerNum: int):  # study if volatility impact the predicted values
        var = {'volatility': [], 'accuracy': [], 'nValues': []}
        for x in range(len(currency)):
            var['volatility'].append(models.volatility(x))

        array = [currency, var['volatility'], var['accuracy'], var['nValues']]


for x in range(3):
    models.volatility(x)
