import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import logging

covergeData = {}

class main:
    def __init__(self) -> None:
        self.historical = list(yf.download("BTC-USD", progress=False, period="12mo", interval="1h")['Close'])
        self.historical.reverse()
    def getData(self, interval):
        covergeData.clear()
        historical = self.historical
        var = {'pattern': [], 'change': [], 'plaid': {}}
        for count in range(len(historical)):
            try:
                dif = historical[count] - historical[count+1]
                if dif >= 0: var['pattern'].append(1)
                else: var['pattern'].append(0)                  #Find Pattern
                change = (historical[count] - historical[count+interval])/historical[count]
                var['change'].append(change)                    #Find Change
            except: pass
        for x in range(len(var['change']), len(var['pattern'])): var['change'].append(0)# make Same Length

        newPattern = []
        newChange = []
        for x in range(len(var['pattern'])):
            patternTempo = []
            changeTempo = []
            for y in range(interval):
                try:
                    patternTempo.append(var['pattern'][x+y])
                    changeTempo.append(var['change'][x+y])
                except: pass
            newPattern.append(str(patternTempo))
            newChange.append(changeTempo)
        var['pattern'] = newPattern
        var['change'] = newChange
        #=================SplitIntoInterval===============
        temporary = []
        for pat in var['pattern']: 
            temporary.append(str(pat))
        var['pattern'] = temporary
        #=============Convert Pattern to Str===========To make in to Dict Key
        for x in range(len(var['pattern'])):
            covergeData.update({var['pattern'][x]: []})
        # ===========Create "Dict" With empty "List"==========
        for x in range(len(var['pattern'])):
            covergeData[var['pattern'][x]].append(np.average(var['change'][x]))

    def predictInterval(interval):
        from datetime import datetime
        from termcolor import colored
        historical = main().historical
        main().getData(interval)
        pattern = []
        for count in range(interval):
            try:
                dif = historical[count] - historical[count+1]
                if dif >= 0: pattern.append(1)
                else: pattern.append(0)
            except:pass
        # print(pattern)
        temporary = []
        for x in range(len(pattern)):
            temporary.append(pattern[x]) #Change to Str
        # pattern = str(temporary).replace(",","")
        # =============Get pattern===========
        prediction = historical[0] + (historical[0] * np.average(covergeData[str(pattern)]))
        until = str(int(datetime.now().strftime("%H")) + interval) + ":" +  datetime.now().strftime("%M")
        print(colored((datetime.now().strftime("%m/%d/%Y %H:%M"), until),"white", "on_green"), 
                colored(" priceInterval", 'red'), interval,">>",round(prediction, 2), 
                colored("Percent", 'blue'), round(np.average(covergeData[str(pattern)])*100, 3))
        return prediction, round(np.average(covergeData[str(pattern)])*100, 3)

    def predict(pattern, price, interval):
        percent = np.average(covergeData[pattern])
        prediction = price +(price * percent)
        return prediction, percent
    
    def plot(interval, plotpercent = False):
        main().getData(interval)
        # get pattern
        historical = main().historical
        # historical = list(yf.download("BTC-USD", progress=False, period="10mo", interval="1h")['Close'])
        # historical.reverse()
        pattern = []
        for count in range(len(historical)):
            try:
                dif = historical[count] - historical[count+1]
                if dif >= 0: pattern.append(1)
                else: pattern.append(0)                  #Find Pattern
            except: pass

        newPattern = []
        for x in range(len(pattern)):
            patternTempo = []
            changeTempo = []
            for y in range(interval):
                try:
                    patternTempo.append(pattern[x+y])
                    changeTempo.append(pattern[x+y])
                except: pass
            newPattern.append(str(patternTempo))
        pattern = newPattern
        #=================SplitIntoInterval===============
        temporary = []
        for pat in pattern:
            temporary.append(str(pat))
        pattern = temporary
        #=============Convert Pattern to Str===========To make in to Dict Key    
        
        pricePredict = []
        percent = []
        from alive_progress import alive_bar
        with alive_bar(len(pattern)) as bar:
            for x in range(len(pattern)):
                # print(pat)
                pricePredict.append(main.predict(pattern[x], historical[x], interval)[0])
                percent.append(main.predict(pattern[x], historical[x], interval)[1])
                bar()
        
        pricePredict.reverse()
        historical.reverse()
        period = 50
        with alive_bar(period) as bar:
            for x in range(1, period+1):
                pricePredict.append(main.predictInterval(x)[0])
                bar()

        if plotpercent==False:
            plt.plot(model.SMA(pricePredict, 12), label='SMA')
            plt.plot(pricePredict, label='Prediction', color='#70FF00')
            plt.plot(historical, label = 'Historical')
            plt.legend()    
        elif plotpercent==True:
            fig, axs = plt.subplots(2)  
            axs[0].plot(model.SMA(pricePredict, 12), label='SMA', color='#70FF00')
            axs[0].plot(historical, label = 'Historical', color='#F79090')
            axs[0].plot(pricePredict, label='Prediction', color='#8A47F8')        
            axs[1].plot(percent)
            axs[0].legend()
        plt.show()

class model:
    def SMA(data, period):
        SMAresult = []
        for x in range(len(data)):
            periodThis = []
            for y in range(period):
                try: periodThis.append(data[x+y])
                except: pass
            SMAresult.append(np.average(periodThis))
        return SMAresult



main.plot(5, plotpercent=True)
