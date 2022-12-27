from model import dollar_cross_averaging
import matplotlib.pyplot as plt
import main

close_price = main.historical["Close"]
function_name = [dollar_cross_averaging]
model_signals = [dollar_cross_averaging.main(data=main.historical)]


for count, model_data in enumerate(model_signals):
    price_gain = []
    save_price:float = None
    for num, i in enumerate(model_data):
        if i == main.buy: save_price = close_price[num]
        elif i == main.sell:
            try:
                different = close_price[num] - save_price
                price_gain.append(different)
                # print(different)
            except: pass
            save_price = None
            
    sum_price_gain, percent_gain = sum(price_gain), (sum(price_gain)/close_price[-1]) * 100
    print(f'\nSummarize data >>> {function_name[count].__name__}\nn_signal: {len(model_data)}  n_close-price: {len(close_price)}',
        f'\nsum_gain : {sum_price_gain} usd   percent_gain : {round(percent_gain, 2)} %')
    plt.show()