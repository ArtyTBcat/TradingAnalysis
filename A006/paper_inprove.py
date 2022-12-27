from model import dollar_cross_averaging
import matplotlib.pyplot as plt
import yfinance as yf
import datetime, main

ticker = "BTC-USD"

total_gain: list = []
end = datetime.datetime.today()
for day in range(1):
    start = end - datetime.timedelta(30)
    historical = yf.download(ticker, start=start,
                            end=end, interval="1h")
    __CLOSE__ = historical["Close"]
    end = end - datetime.timedelta(1)
    print(historical)
    
    model_signal = [dollar_cross_averaging.main(data=historical)]
    SIGNAL = main.signals  # [buy, neutral, sell]
    
    for model in model_signal:
        # cycle through model 
                
        price_gain: list = []
        save_price: float = None
        for num, cycle_signal in enumerate(model):
            if cycle_signal == main.buy:
                save_price = __CLOSE__[num]
            elif cycle_signal == main.sell:                
                gain = __CLOSE__[num] - save_price
                print(
                    f'Gain: {gain: <15} close: {__CLOSE__[num]: ^5} buy: {save_price: ^5}')
                price_gain.append(gain)
                total_gain.append(gain)
                save_price = 0

            # print(price_gain)
        plt.pause(10)
        plt.clf()

current_price = yf.download(ticker, period='1d')['Close'][-1]
print(f'\n{"overall summary":-^30}')
print(f'{"total gain": <15}: {sum(total_gain)}')
print(f'{"Annual % rate": <15}: {sum(total_gain)/current_price*100}')
