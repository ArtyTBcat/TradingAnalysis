import numpy as np

currency = ['BTC','BNB','ETH']

def hisClose(currencyNum: int):
    import yfinance as yf
    historicalReturn = list(yf.download(currency[currencyNum]+'-usd',
                                        progress=False, period='max', interval='1d')['Close'])
    historicalReturn.reverse()
    # historicalReturn.pop(0)
    return historicalReturn

def ndarray(priceClose: list):
    """
    Return
    ------
    return N_sample, N_feature
    ------
    result:
        N_sample >> [array[SumPerChange, AvgPerChg, PuellMultiple] ]
        N_feature >> array[futureVal]
    """
    
    var = {'n_sample':[], 'n_feature':[], 'n_featureFloat': [], 'changeArray': []}
    #           // full array
    
    
    
    # Get full Percent Change Array
    PercentChange = []
    for priceCount in range(len(priceClose)):
        try:
            PercentChg = (priceClose[priceCount] - priceClose[priceCount+1])/priceClose[priceCount+1]*100
            PercentChange.append(PercentChg)
        except:pass
        
                
    
    # Make N_sample
        # - SumPerChange
        # - Average Per Change
        # - Puellmultiple
    # N_feature
        # - feature Value
    Changeinterval = 26
    futureVal = 1
    try:
        for percentCount in range(len(PercentChange)):
            changeArray = []        
            for CIcount in range(Changeinterval):
                changeArray.append(PercentChange[percentCount+CIcount])
                # n_feature Done!!
            if percentCount >= 0:
                var['n_feature'].append(int(PercentChange[percentCount-futureVal]))
                var['n_featureFloat'].append(PercentChange[percentCount-futureVal])
                # print(PercentChange[percentCount-futureVal])
            else: var['n_feature'].append(None), var['n_featureFloat'].append(None)
            SumPerChange = sum(changeArray)
            AvgPerChange = np.average(changeArray)        
            # PuellMultiple
            puellMovingAvg = []
            for x in range(1,len(changeArray)):
                puellMovingAvg.append(changeArray[x])
            PuellMultiple = changeArray[0] / np.average(puellMovingAvg)
            var['n_sample'].append([SumPerChange])
            var['changeArray'].append(changeArray)
            # var['n_sample'].append([SumPerChange])
            # print(SumPerChange, AvgPerChange, PuellMultiple)
    except:pass
    x_test = [var['n_sample'].pop(0)]
    var['n_feature'].pop(0)
    var['n_featureFloat'].pop(0)
        
    return var['n_sample'], var['n_feature'], x_test, var['n_featureFloat'], var['changeArray']
    