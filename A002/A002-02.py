import yfinance as yf
from collections import Counter
import numpy as np
import pandas as pd

data = {'pattern': [], 'count': [], 'probability': []}

historical = list(yf.download("BTC-USD", period="6mo", interval="1h")['Close'])
historical.reverse()
def getData(interval):
    pattern = []
    for count in range(len(historical)):
        try: dif = historical[count] - historical[count+1]
        except: pass
        if dif >= 0:
            pattern.append(1)
        else: pattern.append(0)
    # print((np.array_split(pattern, interval))) 
    SplitIntervalarray = np.array_split(pattern, (len(pattern)/ interval))
    # print(var)
    interPattern = []
    for convertStr in SplitIntervalarray:
        interPattern.append(str(convertStr))
    # print(interPattern)
    a = dict(Counter(interPattern))
    data["pattern"].append(list(a.keys()))
    data["count"].append(list(a.values()))
    # print(pd.DataFrame(data))

def getData2(interval):
    var = {'pattern': [], 'change': []}
    for count in range(len(historical)):
        try:
            dif = historical[count] - historical[count+1]
            if dif >= 0: var['pattern'].append(0)
            else: var['pattern'].append(1)
        # =================find Pattern==============
            change = (historical[count] - historical[count+interval])/historical[count]
            var['change'].append(change)
        # =================find Change================
        except: pass
    # make Same Length
    for x in range(len(var['change']), len(var['pattern'])): var['change'].append(0)

    SplitIntervalarray = np.array_split(list(var['pattern']), (len(var['pattern'])/ interval))
    interPattern = []
    #convert to list
    for convertStr in SplitIntervalarray:
        interPattern.append(str(convertStr))
    data['count'].append(list((Counter(interPattern)).values()))
    data['count'] = data['count'][0]

def getData3(interval):
    var = {'pattern': [], 'change': [], 'plaid': {}}
    for count in range(len(historical)):
        try:
            dif = historical[count] - historical[count+1]
            if dif >= 0: var['pattern'].append(0)
            else: var['pattern'].append(1)                  #Find Pattern
            change = (historical[count] - historical[count+interval])/historical[count]
            var['change'].append(change)                    #Find Change
        except: pass    
    for x in range(len(var['change']), len(var['pattern'])): var['change'].append(0)# make Same Length

    var['pattern'] = np.array_split(list(var['pattern']), (len(var['pattern'])/ interval))
    var['change'] = np.array_split(list(var['change']), (len(var['change'])/ interval))
    #=================SplitIntoInterval===============
    temporary = []
    for pat in var['pattern']: 
        temporary.append(str(pat))
    var['pattern'] = temporary
    #=============Convert Pattern to Str===========To make in to Dict Key


getData2(5)

