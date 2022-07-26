import time
import yfinance as yf
import sqlite3
from binance import Client

client = Client('7n5TvJOJF0A7zKykvw62pqmIoFyluRAneNbjFu3v2jw9FKEJMCirUe4zOvo9KArh', '8N0FnpzwQuELoKaIARZkCAbA9VAym4xTbQQCQxkZ59MNHTHKGZJ4zedzghIuP083')
con = sqlite3.connect('data.db')
cur = con.cursor()


class sqlite():
    def excutemany(tablename, list):
        insert = "insert into "+ tablename + " values (?, ?)"
        cur.executemany(insert, list)
        con.commit()
        
    def exacute(tablename,v1 ,v2):
        insert = "insert into "+ tablename + " values (?, ?)"
        cur.execute(insert, (v1, v2))
        con.commit()
    

class MarketData():
    def __init__(self, ticker):
        # self.price = ((client.get_historical_klines(ticker + 'USDT', Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC"))[0])[1]
        self.historical = yf.download((str(ticker)+'-USD'), period="1y", progress=False, interval="1d")
        self.price = ((client.get_historical_klines(ticker + 'USDT', Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC"))[0])[1]
        time.sleep(0.05)

