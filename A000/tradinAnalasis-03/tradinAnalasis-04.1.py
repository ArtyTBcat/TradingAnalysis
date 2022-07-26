import time
import datetime
from matplotlib import pyplot as plt
from binance import Client
import pandas
from tradingview_ta.main import Interval, TA_Handler

currency = ['BTC','BNB','ETH', 'DOGE','ADA','XRP','SOL','TRX','VET','FTM','DOT','LTC','ATOM']
decimal =  [5,3,4,0,1,0,2,1,1,0,2,3,2]
exchange = 'USDT'
dateback = datetime.datetime(2013,1,1)
plt.figure(figsize=(15, 3))
test = False

def setupNote(key):
    import json
    with open('data/setup.txt', 'r') as f:
        a = json.loads(f.read())[key]
        return a
class openordertext():
    def openorder():
        import json
        with open('data/openorder.txt', 'r') as f:
            a = json.loads(f.read())
            return a
    def writeOpenOrder(myJSONobject):
        import json
        with open("data/openorder.txt", "w") as output:
            json.dump(myJSONobject, output)
    def writeandapend(numlistcurrency):
        lis = openordertext.openorder()
        lis.append(numlistcurrency)
        openordertext.writeOpenOrder(lis)
    def removelist(numlistcurrency):
        lis = openordertext.openorder()
        lis.remove(numlistcurrency)
        openordertext.writeOpenOrder(lis)

client = Client(setupNote('key'), setupNote('secret'))

class data():
    def __init__(self, numlistcurrency):
        coinlong = TA_Handler(symbol=(str(currency[numlistcurrency]) + str(exchange)), screener="crypto", exchange="BINANCE", interval=Interval.INTERVAL_1_MONTH)
        self.summarylong = coinlong.get_analysis().summary
        self.notsummanry = coinlong.get_analysis().summary
        self.RECOMMENDATION = self.summarylong['RECOMMENDATION']
        self.balanceCoin =  client.get_asset_balance(currency[numlistcurrency])['free']
        self.balanceUSDT =  client.get_asset_balance(exchange)['free']
        try: self.price = ((client.get_historical_klines(currency[numlistcurrency] + exchange, Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC"))[0])[1]
        except: self.price = 0

def lastword(string):
    lis = list(string.split(":"))
    length = len(lis)
    return lis[length-1]
def printError():
    import traceback
    print(traceback.format_exc())
    linesend(datetimestrft() + lastword(traceback.format_exc()))
def datetimestrft():
    return datetime.datetime.now().strftime("%d %B %Y // %H:%M:%S")
def linesend(message):
    import numpy as np
    import requests, urllib.parse
    import io
    from PIL import Image
    import os
    token = setupNote('line')
    url = 'https://notify-api.line.me/api/notify'
    HEADERS = {'Authorization': 'Bearer ' + token}
    msg = message
    f = io.BytesIO()
    data = f.getvalue()
    response = requests.post(url,headers=HEADERS,params={"message": msg})

class transaction():
    def buy(numlistcurrency, amountbuy):
        if test == False:
            try: 
                client.create_order(symbol= currency[numlistcurrency] + exchange, side='BUY', type='MARKET', quantity=round(amountbuy, decimal[numlistcurrency])) 
                transaction.printData(numlistcurrency, "BUY" , amountbuy)
                openordertext.writeandapend(numlistcurrency)
            except: printError()
        else:
            print("test")
            try: client.create_test_order(symbol= currency[numlistcurrency] + exchange, side='BUY', type='MARKET', quantity=round(amountbuy, decimal[numlistcurrency])), transaction.printData(numlistcurrency, "BUY" , amountbuy)
            except: printError()
    def sell(numlistcurrency, amountsell):
        if test == False:
            try:
                client.create_order(symbol= currency[numlistcurrency] + exchange, side='SELL', type='MARKET', quantity=round(amountsell, decimal[numlistcurrency]))
                transaction.printData(numlistcurrency, "SELL" , amountsell)
                openordertext.removelist(numlistcurrency)
            except: printError()
        else:
            print("test")
            try:client.create_test_order(symbol= currency[numlistcurrency] + exchange, side='SELL', type='MARKET', quantity=round(amountsell, decimal[numlistcurrency])), transaction.printData(numlistcurrency, "SELL" , amountsell)
            except: printError()
    def printData(numlistcurrency, transactionSTR ,amount):
        printDataFormat = currency[numlistcurrency] ,datetimestrft() ,transactionSTR, amount
        print(printDataFormat)
        linesend(printDataFormat)

def terminalclear():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(0.01)

def getGraph(coin):
    from numpy import average
    import yfinance as yf
    plt.gca().set_ylim([0, 3])
    ticker = yf.download((coin+'-USD'), dateback, datetime.datetime.now())
    puellMultiple = []
    for x in range(31, len(ticker['Close'])):
        past30 = []
        for y in range(x - 30, x):
            past30.append(ticker['Close'][y])
        puellMultiple.append(average(past30) / ticker['Close'][x])
    plt.plot(puellMultiple, color = '#340B8C')
    plt.title(coin+'-USD')
    plt.show()
    print("")

def getRECCOMENDATION(numlistcurrency):
    from numpy import average
    import yfinance as yf    
    ticker = yf.download((str(numlistcurrency)+'-USD'), dateback, datetime.datetime.now(), progress=False, interval="1d")
    plt.gca().set_ylim([0, 2.5])
    puellMultiple = []
    for x in range(31, len(ticker['Close'])):
        past30 = []
        for y in range(x - 30, x):
            past30.append(ticker['Close'][y])
        puellMultiple.append(average(past30) / ticker['Close'][x])
    plt.plot(puellMultiple, color = '#FBE55A')
    buyvalue = average(puellMultiple) - (average(puellMultiple)* 15) /100 
    sellvalue = average(puellMultiple) + (average(puellMultiple)* 38) /100
    if puellMultiple[len(puellMultiple)-1]< buyvalue: return {"COIN": numlistcurrency,"RECCOMMENDATION": "BUY", "CURRENT": puellMultiple[len(puellMultiple)-1], "AVERAGE": average(puellMultiple), "BUY_AT": buyvalue, "SELL_AT": sellvalue}
    elif puellMultiple[len(puellMultiple)-1] > sellvalue: return {"COIN": numlistcurrency, "RECCOMMENDATION":"SELL", "CURRENT": puellMultiple[len(puellMultiple)-1], "AVERAGE": average(puellMultiple), "BUY_AT": buyvalue, "SELL_AT": sellvalue}
    else: return {"COIN": numlistcurrency, "RECCOMMENDATION":"NUETRAL", "CURRENT": puellMultiple[len(puellMultiple)-1], "AVERAGE": average(puellMultiple), "BUY_AT": buyvalue, "SELL_AT": sellvalue}

class longstart():
    def strat(limitopenorder):
        print(datetimestrft(), ">>> OpenOrder:", len(openordertext.openorder()), "// LimitOpenOrder:", limitopenorder ,"\n")
        df = []
        for x in range(len(currency)):
            df.append(getRECCOMENDATION(currency[x]))
            if len(openordertext.openorder()) < int(limitopenorder) and all(t in openordertext.openorder() for t in [x]) == False:
                if getRECCOMENDATION(currency[x])["RECCOMMENDATION"] == "BUY":
                    amountbuy = ((float(data(x).balanceUSDT)*((setupNote('percent')* (len(openordertext.openorder()) + 1))/100)) / float(data(x).price))
                    print(getRECCOMENDATION(currency[x]))
                    transaction.buy(x, amountbuy)
        for x in range (len(openordertext.openorder())):
                if getRECCOMENDATION(currency[x])["RECCOMMENDATION"] == "SELL":
                    print(getRECCOMENDATION(currency[x]))
                    for d in range(decimal[openordertext.openorder()[x]]): minus = minus / 10
                    amountsell = (float(data(openordertext.openorder()[x]).balanceCoin) - minus)
                    transaction.sell(openordertext.openorder()[x], amountsell)
        print(pandas.DataFrame(data=df))        


def typecommand(waitsec):
    import keyboard
    print("\n")
    for x in range((int(waitsec))*10):
        print("press Ctrl+Shift+A >>> Access command // SecCount ", x/10, "seconds", end="\r")
        if keyboard.is_pressed('ctrl+shift+a'):
            command = input("\ntradingAnalasis-04.py>>>   ")
            if command == 'plot':
                command = input("   coin>>> ")
                getGraph(command)
            else: pass
        else: pass
        time.sleep(0.1)

while True:
    try:
        longstart.strat(setupNote('limitOrder'))        
        typecommand(60)
        terminalclear()
    except:
        printError()
    
