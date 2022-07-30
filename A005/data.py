import yfinance as yf
import numpy as np
import pandas as pd
from A004_copy.A004_01 import main as A004Main

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
        return vol


class collections:
    def volatility():  # study if volatility impact the predicted values
        var = {'predicted': [], 'volatility': [],
               'accuracy': [], 'nValues': []}
        try:
            df = pd.read_csv('data.csv')
            dataRead = df.to_dict()
        except:
            df = pd.DataFrame(var)
            df.to_csv('data.csv')

        for x in range(len(currency)):
            PREDICTED = A004Main(x)['predictedPrice']
            var['predicted'].append(PREDICTED)
            var['volatility'].append(models.volatility(x))

            accuracy = (
                (APIdata(x)[0] - dataRead['predicted'][x]) / dataRead['predicted'][x]) * 100
            xAccuracy = (
                ((dataRead['accuracy'][x] * dataRead['nValues'][x]) + accuracy) / dataRead['nValues'][x])
            var['accuracy'].append(xAccuracy)

            try:
                var['nValues'].append(dataRead['nValues'][x] + 1)
            except:
                var['nValues'].append(1)
        df = pd.DataFrame(var)
        df.to_csv('data.csv')

        print(pd.read_csv('data.csv'))


collections.volatility()
