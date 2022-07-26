from math import sqrt
from data import MarketData
import numpy


def EMA(ticker):
    markt = MarketData(ticker).historical['Close']
    result = (((len(markt)+1)/2)* (float(MarketData(ticker).price) - numpy.average(markt))) + numpy.average(markt)
    return result
def SMA(ticker):
    markt = MarketData(ticker).historical['Close']
    result = numpy.average(markt)
    return result
def vwma(ticker):
    var = {'fraction': [], 'portion' : []}
    markt = MarketData(ticker).historical
    for x in range(len(markt['Close'])):
        var['fraction'].append(float(markt['Close'][x]) * float(markt['Volume'][x]))
        var['portion'].append(markt['Volume'][x])
    result = sum(var['fraction'])/ sum(var['portion'])
    return result
def WMA(ticker):
    var = {'fraction': [], 'portion' : []}
    markt = MarketData(ticker).historical['Close']
    for x in range(len(markt)):
        var['fraction'].append(markt[x] * (len(markt)-x))
    var['portion'].append((x * (x+1))/2)
    result = sum(var['fraction']) / sum(var['portion'])
    return result
def HMA(ticker):
    markt = MarketData(ticker).historical['Close']
    var = {'fraction': [], 'portion' : []}
    WMAA = WMA(ticker)
    bruh = float(WMAA)* (2*float(WMAA)*(len(markt)) - (float(WMAA)*len(markt)) )
    var['fraction'].append(bruh)
    var['portion'].append(sqrt(len(markt)))
    result = sum(var['fraction']) / sum(var['portion'])
    return result

def PM(ticker):
    markt = MarketData(ticker).historical['Close']
    var = {'PM' : [], 'past': []}
    for x in range(30, len(markt)):
            var['past'] = []
            for y in range(x - int(30), x):
                var['past'].append(markt[y])
            var['PM'].append(numpy.average(var['past']) / markt[x])            
    # plt.plot(var['PM']), plt.gca().invert_yaxis(), plt.show()
    result = var['PM'][len(var['PM'])-1]
    return result

# df = pandas.DataFrame({'name': ['EMA', 'SMA', 'vwma', 'WMA', 'HMA', 'PM'], 'matrics': [EMA('BTC'), SMA('BTC'), vwma('BTC'), WMA('BTC'), HMA('BTC'), PM('BTC')]})

# print(df)

