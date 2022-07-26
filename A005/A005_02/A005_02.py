# from A005_02 import model
import model
import yfinance as yf

currency = ['BTC', 'BNB', 'ETH']
hisClose = list(yf.download(currency[0]+'-USD', period='max', interval='1d', progress=False)['Close'])
hisClose.reverse()

print(hisClose)
model.fgik(hisClose)
