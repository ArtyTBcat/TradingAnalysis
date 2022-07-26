from numpy import append, average
import yfinance as yf
import pandas as pd
import os

models = {'rs': [], 'rsi':[], 'pul': [], 'momentum': []}

def historical(ticker):
    return yf.download(ticker+'-USD', progress=False, interval="1d", period="6mo")

class excel:
    def write(excelFile, dict):
        df = pd.DataFrame(dict)
        writer = pd.ExcelWriter(os.path.join('data/',excelFile+'.xlsx'), engine='xlsxwriter')
        os.path.join('data/',excelFile,'.xlsx')
        df.to_excel(writer,sheet_name='Sheet1')
        writer.save()

    def arrange(currency):
        DataFrame = {}
        DataFrame.update(historical(currency))
        DataFrame.update(models)
        excel.write("test"+ currency , DataFrame) #get yf Data to Excel
        



class model:
    def rs(currency, period_day,):        
        var = {'gain': [], 'loss': []}
        data = historical(currency)
        for ProfLossVar in range(len(data['Close'])):
            calui = data['Close'][ProfLossVar] - data['Close'][ProfLossVar-period_day]
            if calui >= 0: var['gain'].append(calui)
            else: var['loss'].append(calui*-1)
            models['rs'].append(average(var['gain'])/average(var['loss']))
        # RSI Value
        for rsicount in range(len(models['rs'])):
            try:
                rsi = 100-(100/(1+models['rs'][rsicount]) )
                models['rsi'].append(rsi)
            except: models['rsi'].append("nan")
    def pul(currency):
        data = historical(currency)
        issued = average(data['Close'])
        for daily in data['Close']:
            puell = daily/issued
            models['pul'].append(puell)
    def momentum(currency, period_day):
        data = historical(currency)['Close']
        for moment in range (len(data)):
            try:
                result = data[moment] - data[moment - period_day]
                models['momentum'].append(result)
            except: result = None



def runmodel():
    model.rs("BTC", 1)
    model.pul("BTC")
    model.momentum("BTC", 1)

runmodel()
excel.arrange("BTC")

