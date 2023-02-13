import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def trading_strategy(prices, window=14):
    signals = np.zeros(len(prices))
    X = np.zeros((len(prices), window))
    y = np.zeros(len(prices))
    
    for i in range(window, len(prices)):
        X[i, :] = prices[i-window:i]
        y[i] = np.sign(prices[i] - prices[i-1])
        
    X_train = X[window:, :]
    y_train = y[window:]
    X_test = X[:window, :]
    
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    signals[:window] = predictions
    
    return signals
