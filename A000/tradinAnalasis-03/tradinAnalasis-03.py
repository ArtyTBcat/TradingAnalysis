from binance import Client
from tradingview_ta.main import Interval, TA_Handler
import datetime
import time


currency = ['BTC','BNB','ETH','ADA','XRP','SOL','TRX','VET','FTM','DOT','LTC','ATOM']
decimal =  [5,3,4,1,0,2,1,1,0,2,3,2]
exchange = 'USDT'
test = False

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
def setupNote(key):
    import json
    with open('data/setup.txt', 'r') as f:
        a = json.loads(f.read())[key]
        return a
        
client = Client(setupNote('key'), setupNote('secret'))

def printError():
    import traceback
    print(traceback.format_exc())
    linesend(datetimestrft() + " " +  "*" + last2word(traceback.format_exc()) + "*")
    pass
def datetimestrft():
    return datetime.datetime.now().strftime("%d %B %Y // %H:%M:%S")
def last2word(string):
    lis = list(string.split(":"))
    length = len(lis)
    return lis[length - 1]

class data():
    def __init__(self, numlistcurrency):
        coinlong = TA_Handler(symbol=(str(currency[numlistcurrency]) + str(exchange)), screener="crypto", exchange="BINANCE", interval=Interval.INTERVAL_1_MONTH)
        self.summarylong = coinlong.get_analysis().moving_averages
        self.notsummanry = coinlong.get_analysis().summary
        self.RECOMMENDATION = self.summarylong['RECOMMENDATION']
        self.balanceCoin =  client.get_asset_balance(currency[numlistcurrency])['free']
        self.balanceUSDT =  client.get_asset_balance(exchange)['free']
        try: self.price = ((client.get_historical_klines(currency[numlistcurrency] + exchange, Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC"))[0])[1]
        except: self.price = 0
        time.sleep(0.01)

def linesend(message):
    try:
        import requests
        import io
        token = setupNote('line')
        url = 'https://notify-api.line.me/api/notify'
        HEADERS = {'Authorization': 'Bearer ' + token}
        msg = message
        f = io.BytesIO()
        f.getvalue()
        requests.post(url,headers=HEADERS,params={"message": msg})
    except:
        pass

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


class longStrat():
    def strat01(limitopenorder):
        performance().start()
        monitor().analize()
        print(datetimestrft(), "OpenOrder:", len(openordertext.openorder()), "// LimitOpenOrder:", limitopenorder)
        for x in range (len(currency)):
            print("                   ",currency[x], data(x).notsummanry,"        ", end="\r")
            if len(openordertext.openorder()) < int(limitopenorder) and all(t in openordertext.openorder() for t in [x]) == False:
                REC = data(x).RECOMMENDATION
                if REC == 'STRONG_BUY' and (data(x).notsummanry['RECOMMENDATION'] == 'BUY' or data(x).notsummanry['RECOMMENDATION'] == 'STRONG_BUY'):
                    amountbuy = ((float(data(x).balanceUSDT)*((setupNote('percent')* (len(openordertext.openorder()) + 1))/100)) / float(data(x).price))
                    transaction.buy(x, amountbuy)
        for x in range (len(openordertext.openorder())):
            REC = data(openordertext.openorder()[x]).RECOMMENDATION
            if REC == 'STRONG_SELL' and (data(x).notsummanry['RECOMMENDATION'] == 'SELL' or data(x).notsummanry['RECOMMENDATION'] == 'STRONG_SELL'):
                for d in range(decimal[openordertext.openorder()[x]]): minus = minus / 10
                amountsell = (float(data(openordertext.openorder()[x]).balanceCoin) - minus)
                transaction.sell(x, amountsell)
        performance().returnend()

class performance():
    def start(self):
        global starttime
        starttime = time.time()
    def returnend(self):
        endtime = time.time() - starttime
        influx().performanceinflux(endtime)
        return endtime

class monitor():
    def analize(self):
        import pandas
        datdata = {'COIN':[], 'RECOMMEN': [], 'BUY':[],'NEU': [], 'SELL':[]}
        for x in range(len(currency)):
            REC = data(x).summarylong
            datdata['COIN'].append(currency[x])
            datdata['RECOMMEN'].append(REC['RECOMMENDATION'])
            datdata['BUY'].append(REC['BUY'])
            datdata['NEU'].append(REC['NEUTRAL'])
            datdata['SELL'].append(REC['SELL'])
            influx().printinflux(REC['RECOMMENDATION'], x)
        dataframe = pandas.DataFrame(data=datdata)
        monitor().clear()
        print(datetime.datetime.now().strftime("%d %B %Y // %H:%M:%S"),">>>")
        print(dataframe)
        print()
    def clear(self):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(0.01)
        
class influx(object):
    def __init__(self):
        from influxdb_client.client.write_api import SYNCHRONOUS
        from influxdb_client import InfluxDBClient, Point, WritePrecision
        token = setupNote('influx')
        self.org = "crypto"
        self.bucket = "crypto-data-bucket"
        self.influxclient = InfluxDBClient(url="http://localhost:8086", token=token)
        self.write_api = self.influxclient.write_api(write_options=SYNCHRONOUS)
    def performanceinflux(self, value):
        try:
            data = ["crypto "+ "performance"+ "=" + str(value)]
            self.write_api.write(self.bucket, self.org, data)
        except:
            import subprocess
            subprocess.Popen([r"data\server-run.bat"])
            time.sleep(5)
    def printinflux(self, RECOMMENDATION, numlistcurrency):
        if RECOMMENDATION == 'STRONG_SELL':u = -2
        elif RECOMMENDATION == 'SELL':u = -1
        elif RECOMMENDATION == 'BUY':u = 1
        elif RECOMMENDATION == 'STRONG_BUY':u = 2
        else:u = 0
        try:
            data = ["crypto "+ currency[numlistcurrency]+ "=" + str(u)]
            self.write_api.write(self.bucket, self.org, data)
        except:
            import subprocess
            subprocess.Popen([r"data\server-run.bat"])
            time.sleep(5)
linesend("*" + str(datetimestrft()) +"*"+ " PROGRAM_START")
while True:
    try:longStrat.strat01(setupNote('limitOrder')), time.sleep(150)
    except: printError()
