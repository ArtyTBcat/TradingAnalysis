from numpy import average
import matplotlib.pyplot as plt
import numpy as np

interval = 10
futureInter = 3

def fgik(closePrice: list):
    #g get SPC AVG.CHG, Puell
    var = {'n_sample': [], 'n_feature': []}
    try:
        for CPcount in range(len(closePrice)):
            chgArrayInteval = []
            for interCount in range(interval):
                newPrice = closePrice[CPcount+interCount]
                oldPrice = closePrice[CPcount+interCount+1]
                chg = (newPrice-oldPrice)/oldPrice * 100
                chgArrayInteval.append(chg)        
            ##n_feature##
            try:
                futureSumThis = []
                for x in range(futureInter):
                    futureSumThis.append(closePrice[CPcount-x])
                futurnew = np.average(futureSumThis)
                futurold = closePrice[CPcount]
                futureChg = (futurnew - futurold)/futurold*100
                var['n_feature'].append(futureChg)
            except: pass        
            ### n_sample ###
            sumPerChg = sum(chgArrayInteval)
            var['n_sample'].append(sumPerChg)
            avgChg = average(chgArrayInteval)
            # print(sumPerChg, avgChg)
    except: pass
    plt.scatter(x=var['n_sample'], y=var['n_feature'])
    plt.show()
