import numpy as np

def trading_strategy(prices, window=100):
    signals = np.zeros(len(prices))
    mean = np.zeros(len(prices))
    threshold = 0.02
    
    for i in range(window-1, len(prices)):
        mean[i] = np.mean(prices[i-window+1:i+1])
        
        if prices[i] > mean[i] + mean[i] * threshold:
            signals[i] = -1
        elif prices[i] < mean[i] - mean[i] * threshold:
            signals[i] = 1
        else:
            signals[i] = 0
            
    return signals
