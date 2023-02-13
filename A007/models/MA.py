import numpy as np

def trading_strategy(prices, short_window=50, long_window=200):
    signals = np.zeros(len(prices))
    short_ma = np.zeros(len(prices))
    long_ma = np.zeros(len(prices))
    
    for i in range(long_window-1, len(prices)):
        short_ma[i] = np.mean(prices[i-short_window+1:i+1])
        long_ma[i] = np.mean(prices[i-long_window+1:i+1])
        
        if short_ma[i] > long_ma[i]:
            signals[i] = 1
        elif short_ma[i] < long_ma[i]:
            signals[i] = -1
        else:
            signals[i] = 0
            
    return signals