from model import __config__
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString

plt.ylabel('price')
plt.xlabel('time')
n_factor: int = 10

def main(data):
    close_prices = list(data["Close"])
    return_values: list = []
    p_chunks = []
    MA_: list = []
    for num, price in enumerate(close_prices):
        n_factor_chunks = close_prices[num - int(len(close_prices)/n_factor): num]
        moving_average = np.average(n_factor_chunks)
        MA_.append(moving_average)
        p_chunks.append(n_factor_chunks)
        
        # Buy and Sell signal
    
    last_bought:float = None
    open_order: int = 0
    for num, i in enumerate(close_prices):
            MA_line = LineString([(num-1, MA_[num-1]), (num, MA_[num-1])])
            price_coordinates = (num-1, close_prices[num-1]), (num, i)
            line_price = LineString(price_coordinates)
            int_pt = MA_line.intersection(line_price)
            if len(np.array(int_pt)) != 0 and num!=0:
                slope = (close_prices[num-2] - close_prices[num]) / (1)
                up_down = calculate_slope_traject(slope)
                x, y = np.array(int_pt)
                if up_down is "up" and open_order == 0: 
                    return_values.append(__config__.buy)
                    plt.plot([x], [y], "bo", color="#78FF00")
                    last_bought = i
                    open_order += 1
                elif up_down is "down" and open_order >= 1 and i > last_bought:
                    return_values.append(__config__.sell)
                    plt.plot([x], [y], "bo", color="#BB0000")
                    open_order = 0
                else: return_values.append(__config__.neutral)
                print(f'{num} slope: {slope:15f} is {up_down}')
                
                # plt.annotate(str(num), (x, y))
            else: return_values.append(__config__.neutral)
    plt.plot(close_prices, color="#1E5CFF")
    plt.plot(MA_, color="#E3EC28")
    
    # plt.show()
    return return_values
    
    
def calculate_slope_traject(slope: float):
    if slope < 1:
        return "up"
    else: return "down"