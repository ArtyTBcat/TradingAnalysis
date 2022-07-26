from models import EMA, SMA, vwma, WMA, HMA, PM

model = [EMA, SMA, vwma, WMA, HMA, PM]

for x in range(len(model)):
    print(model[x]('BTC'))