import yfinance as yf
from numpy import average
import numpy as np
import matplotlib.pyplot as plt

# pattern: count
# [0, 1, 0, 1]: 10
probabilityData = {}
data = {'predict': []}
accuracyData = {}


historical = yf.download("BTC-USD", period="1y", interval="1h")['Close']

def pattern(predictinter, interval = int(4)):
    for x in range(len(historical)):
        pattern = []
        for interv in range(interval): #find patterns
            try:
                dif = historical[interv+x] - historical[(interv+x)-1]
            except: pass
            if dif >= 0: pattern.append(1)
            else: pattern.append(0)
            prodata = []
            for getprobability in range(predictinter):
                try:
                    probability = (historical[interv+x+getprobability]
                                     - historical[interv+x])/ historical[interv+x]
                    prodata.append(probability)
                except: pass

        if str(pattern) in data.keys():#add pattern
            data.update({str(pattern): data[str(pattern)]+1})
            try: 
                newprobability = ((probabilityData[str(pattern)] * data[str(pattern)])
                                     + probabilityData[str(pattern)])/data[str(pattern)]
                probabilityData.update({str(pattern): newprobability})
            except: pass
        else: data.update({str(pattern): 1}), probabilityData.update({str(pattern): average(prodata)}), accuracyData.update({str(pattern): []})

    #print pretty Data
    # for key in probabilityData:
    #     print(key, "cont:", data[key], "prob:", probabilityData[key])

def predictReal(interval):
    historical = yf.download("BTC-USD", period="1wk", interval="1h")['Close']
    for x in range(len(historical)):#Get pattern
        pattern = []
        for interv in range(interval): #find patterns
            try:
                dif = historical[interv+x] - historical[(interv+x)-1]
            except: pass
            if dif >= 0: pattern.append(1)
            else: pattern.append(0)

        try:
            predicted = historical[x+interv]+ (historical[x+interv] * (probabilityData[str(pattern)]/100))
            data["predict"].append(predicted)
        except: pass
    fig, axs = plt.subplots(2)
    axs[0].set_title("Prediction")
    axs[1].set_title("Real Price")
    axs[0].plot(data["predict"])
    axs[1].plot(historical)
    plt.show()

    
    # print(pd.DataFrame(data["predict"]))


def future(interval, daypredict): #Do not copy
    historical = list(yf.download("BTC-USD", period="1d", interval="1h")['Close'])
    pattern = []
    for x in range(len(historical)):#Get pattern        
        for interv in range(interval): #find patterns
            try:
                dif = historical[interv*x] - historical[(interv*x)-1]
            except: pass
            if dif >= 0: pattern.append(1)
            else: pattern.append(0)
    pattern = (np.array_split(pattern, interval))
    
    historical.reverse()
    print(list(pattern[0]))
    predicted = historical[0]+ (historical[0] * (probabilityData[str(list(pattern[0]))]/100))
    
    plt.plot((historical, predicted))
    plt.show


pattern(6, interval= 6)
# predictReal(6)
future(6, 6)
