import yfinance as yf
import numpy as np
import pandas as pd
from termcolor import colored
from datetime import datetime
import matplotlib.pyplot as plt
import time
from colorama import init

init()

data = {'pattern': [], 'count': [], 'probability': []}
covergeData = {}

historical = list(yf.download("BTC-USD", progress=False, period="12mo", interval="1h")['Close'])
historical.reverse()

class main:
    def getData(interval):
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

    def predict(interval):
        main.getData(interval)     
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

def dataAnalysis():
    import sqlite3
    con = sqlite3.connect('priceAnalytics.db')
    cur = con.cursor()
    # cur.execute('''CREATE TABLE price
    #            (date text, predictFFS text)''')  ##create Table
    # make many hour to list
    
    predictionlist = [historical[0]]
    percent = [None]
    for x in range(1,12):
        varrun = main.predict(x)
        predictionlist.append(varrun[0])
        percent.append(varrun[1])


    cur.execute("insert into price values (?, ?, ?)", (datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                 str(predictionlist), str(percent)))

    print("\n", datetime.now().strftime("%m/%d/%Y %H:%M:%S"), "SavingData...\n")
    con.commit()
    con.close()

# def run():    
#     XAxis = ['now']
#     plotlis = [historical[0]]
#     for x in range(4,8):
#         plotlis.append(main.predict(x))
#         XAxis.append(x)
#         # plt.plot(main.predict(x))
#     plt.title("Next 7 hour price")
#     plt.plot(XAxis, plotlis)
#     plt.show()

# run()
# main.predict(5)

dataAnalysis()
time.sleep(300)


