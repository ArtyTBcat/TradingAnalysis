import yfinance as yf
import logging
import numpy as np
import pandas as pd

logging.basicConfig(filename='A003.log', encoding='utf-8', level=logging.DEBUG)

class main:
    def __init__(self):
        self.historical = list(yf.download("BTC-USD", progress=False, period="12mo", interval="1h")['Close'])
        self.historical.reverse()
    def TrainAlgo(self, interval, nextHour):
        patternData = pattern.patternIntervalDataSet(interval)
        changeDataListWithPatternKeys = pattern.getData(interval, nextHour)
        price = self.historical
        retuen_predictionList = []
        for x in range(len(patternData)):
            percentDifferentData = np.average(changeDataListWithPatternKeys[patternData[x]])
            prediction = price[x] + (price[x]*percentDifferentData/100)
            retuen_predictionList.append(prediction)
        return retuen_predictionList
    def predictFuture(self, interval, nextHour, amountHourPredict):
        price = list(self.historical)
        allPattern = list(pattern.patternIntervalDataSet(interval)[1]) #Append Latest Data To here
        trainedData = pattern.getData(interval, nextHour)
        pltPrediction = []
        for x in range(amountHourPredict):
            thisisNowTheLatestPattern = pattern.convertDataToInterval(allPattern, interval)[0]
            percentDifferentData = np.average(trainedData[thisisNowTheLatestPattern]) #uncomment if need to be fast
            # percentDifferentData = np.average(pattern.getData(interval, nextHour)[thisisNowTheLatestPattern])
            predict = price[0] + (price[0]*percentDifferentData/100)
            if predict >= price[0]:
                allPattern.insert(0, 1)
            else: allPattern.insert(0, 0)
            price.insert(0, predict)
            print(predict, thisisNowTheLatestPattern, percentDifferentData)
            pltPrediction.append(percentDifferentData)
            # next Append Pattern Data
        import matplotlib.pyplot as plt
        plt.plot(pltPrediction)
        plt.show()        

class pattern:
    def patternIntervalDataSet(interval):
        logging.debug('running PatternIntervalDataSet')
        priceData = main().historical
        patternDataAll = []
        for x in range(len(priceData)):
            different = priceData[x] - priceData[x-1]
            if different >= 0: patternDataAll.append(1)
            else: patternDataAll.append(0)
        patternDataset = pattern.convertDataToInterval(patternDataAll, interval)
        return patternDataset, patternDataAll
    def changeIntervalDataSet(interval, nextPriceIntervalDay):
        logging.debug('running changeIntervalDataSet')
        priceData = main().historical
        return_change = []
        try:
            for historicalCount in range(len(priceData)):
                nextPeriodDay =  priceData[historicalCount+nextPriceIntervalDay]
                percentChange = ((priceData[historicalCount] - nextPeriodDay)/nextPeriodDay)*100
                return_change.append(percentChange)
        except: pass
        return return_change
    def convertDataToInterval(data, interval):
        # Return Patterns
        logging.debug('running ConvertDataToInterval')
        return_data = []
        try:
            for countData in range(len(data)):
                pattern = []
                for countInterval in range(interval):
                    pattern.append(data[countData+countInterval])
                return_data.append(str(pattern))
        except: pass
        return return_data    
    def getData(interval, nextDay):
        covergeData = {}
        var = {'pattern': pattern.patternIntervalDataSet(interval)[0], 'change': pattern.changeIntervalDataSet(interval, nextDay)}
        for x in range(len(var['pattern'])):
            covergeData.update({var['pattern'][x]: []})
        # ===========Create "Dict" With empty "List"==========
        try:
            for x in range(len(var['pattern'])):
                covergeData[var['pattern'][x]].append(var['change'][x])
        except: pass
        return covergeData

main().predictFuture(6, 1, 100)
