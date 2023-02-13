import numpy as np
import pandas as pd

#convert list to pattern Interval
def pattern(data:list, interval:int, forwardForcast:int):
    returnPattern = []
    returnFutureChange = []
    try:
        for rangeData in range(len(data)):
            pattern = []            
            for interValCount in range(interval):
                pattern.append(data[rangeData+interValCount])
            returnPattern.append(pattern)
            if rangeData-forwardForcast >= 0:
                returnFutureChange.append(np.average(returnPattern[rangeData-forwardForcast]))
            else: returnFutureChange.append(None)
    except: pass
    return returnPattern, returnFutureChange

# This will make historical to a list of percent Change
def percentConvet(data:list):
    percentReturn = []
    try:
        for hisCount in range(len(data)):
        
            newPrice = data[hisCount]
            oldPrice = data[hisCount+1]
            percentChange = ((newPrice - oldPrice)/oldPrice)*100
            roundedPercentChange = np.round(percentChange, 2)

            percentReturn.append(roundedPercentChange)
    except:pass
    return percentReturn

def methodSPC(data:list, interval: int, forwardForcast: int):
    dataList = []
    dataDictForm = {'SumPerChg':[], 'PerChgList':[], 'avgPerChgList':[], 'FutureChg':[]}
    # dataList in list from [  [SumPerChg, PercentChange, AVGPerChange, FutureChg], [SumPerChg, PercentChange, AVGPerChange, FutureChg] ]
    percentChangeList = pattern(percentConvet(data), interval, forwardForcast)
    x=0
    for cyclePerChgList in percentChangeList[0]:
        SPC = round(sum(cyclePerChgList), 3)
        PerChgList = cyclePerChgList
        avgPerChgList = np.average(cyclePerChgList)
        dataList.append([SPC, PerChgList, avgPerChgList, percentChangeList[1][x]])
        dataDictForm['SumPerChg'].append(SPC)
        dataDictForm['PerChgList'].append(PerChgList)
        dataDictForm['avgPerChgList'].append(avgPerChgList)
        dataDictForm['FutureChg'].append(percentChangeList[1][x])
        x+=1
    printdataframe = pd.DataFrame(dataList)
    printdataframe.columns = ['SumPerChg','PercentChange','AVGPerChange','FutureChg']
    # print(printdataframe)
    return dataList, dataDictForm
    
def groupData(data:list, spacing: int):
    #makeData To group
    SumPerChg = []
    for x in data:
        SumPerChg.append(x[0])
    SumPerChg.sort()
    # import matplotlib.pyplot as plt
    # plt.plot(SumPerChg)
    # plt.show()
    SumPerChgSpacing = []
    for u in range(int(SumPerChg[0]-spacing), int(SumPerChg[-1]+spacing), spacing):
        SumPerChgSpacing.append(u)
    # print(SumPerChgSpacing)
    
    # cycleThoughGroups
    dataSet = []
    for cycleGroups in range(1, len(SumPerChgSpacing)):
        addThisToDataSet = []
        for listInData in data:
            if SumPerChgSpacing[cycleGroups-1] < listInData[0] < SumPerChgSpacing[cycleGroups]:
                addThisToDataSet.append(listInData)
                # addThisToDataSet.append(x[0])
        dataSet.append(addThisToDataSet)
    
    var = {"SumPerChg":[],"FutureChange": []}
    for x in dataSet:
        for i in x:
            try:var['FutureChange'].append(float(i[3])), var['SumPerChg'].append(float(i[0]))
            except:pass
    
    #plotStage
    # from sklearn.linear_model import LinearRegression
    # model = LinearRegression()
    # arrDataSet = {'SumPerChg': np.array(var['SumPerChg']), 'FutureChg': np.array(var['FutureChange'])}
    # model.fit(arrDataSet['SumPerChg'].reshape(1,-1), arrDataSet['FutureChg'].reshape(1,-1))
    

        

