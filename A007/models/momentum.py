import numpy as np

def trading_strategy(prices, lookback=14):
    signals = np.zeros(len(prices))
    momentum = np.zeros(len(prices))
    
    for i in range(lookback, len(prices)):
        momentum[i] = prices[i] - prices[i-lookback]
        
        if momentum[i] > 0:
            signals[i] = 1
        else:
            signals[i] = -1
            
    return signals
