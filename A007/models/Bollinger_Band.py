import numpy as np
import pandas as pd

def trading_strategy(prices, window=20):
    signals = np.zeros(len(prices))
    rolling_mean = np.zeros(len(prices))
    rolling_std = np.zeros(len(prices))
    upper_band = np.zeros(len(prices))
    lower_band = np.zeros(len(prices))
    threshold = 2
    
    for i in range(window-1, len(prices)):
        rolling_mean[i] = np.mean(prices[i-window+1:i+1])
        rolling_std[i] = np.std(prices[i-window+1:i+1])
        upper_band[i] = rolling_mean[i] + rolling_std[i] * threshold
        lower_band[i] = rolling_mean[i] - rolling_std[i] * threshold
        
        if prices[i] > upper_band[i]:
            signals[i] = -1
        elif prices[i] < lower_band[i]:
            signals[i] = 1
        else:
            signals[i] = 0
            
    return signals
