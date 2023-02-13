import yfinance
from models import MA, momentum, sklearn, mean_reversion, Bollinger_Band
import matplotlib.pyplot as plt

his = yfinance.download("BTC-USD", interval="1h", period="1mo")["Close"]

models_output = [MA.trading_strategy(his), momentum.trading_strategy(his), mean_reversion.trading_strategy(his), Bollinger_Band.trading_strategy(his)
                    , sklearn.trading_strategy(his)]
labels = ["moving_average", "momentum", "mean_reversion", "Bullinger Band", "sklearn"]
model_profit:list = []

class signal_paper:
    buy_signal, sell_signal = 1, -1
    latest_buy_price : float = None
    profit:list = []
    STATUS = None
    print("calculating...function", end="\r")
    def buy(current_price):
        # check STATUS
        if signal_paper.STATUS != signal_paper.buy_signal:
            signal_paper.latest_buy_price = current_price
            signal_paper.STATUS = signal_paper.buy_signal

    def sell(current_price):
        if signal_paper.STATUS != signal_paper.sell_signal:
            while signal_paper.latest_buy_price != None:
                profit = current_price - signal_paper.latest_buy_price
                signal_paper.profit.append(profit)
            signal_paper.STATUS = signal_paper.sell_signal    

    def reset():
        print("calculating profits")
        model_profit.append(sum(signal_paper.profit))
        print("---reseting all value in signal paper---")
        signal_paper.latest_buy_price = None
        signal_paper.profit = []
        signal_paper.STATUS = None
 

fig, axs = plt.subplots(6)

axs[0].plot(his)
for num, i in enumerate(models_output):
    # loop in outputs
    for count, signal in enumerate(i):
        if signal == signal_paper.buy_signal: signal_paper.buy(his[count])
        elif signal == signal_paper.sell_signal: signal_paper.sell(his[count])
    signal_paper.reset()
    axs[num+1].plot(i, label =labels[num])
    print(i)

print(model_profit)
plt.show()



