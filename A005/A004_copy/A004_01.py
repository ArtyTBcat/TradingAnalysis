from A004_copy import model
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

currency = ['BTC', 'ETH', 'BNB']


def APIdata(tickerNum: int):  # DataSet historical[1],
    historicalClose = list(yf.download(
        currency[tickerNum] + '-USD', period='max', interval='1d', progress=False)['Close'])
    historicalClose.reverse()
    return historicalClose


def main(tickerNum: int):
    interval = 26
    futureForcast = 1

    proccesModel = model.methodSPC(APIdata(tickerNum), interval, futureForcast)
    model.groupData(proccesModel[0], 3)  # test
    dataSet = pd.DataFrame(proccesModel[1])

    from sklearn.linear_model import LinearRegression
    regresModel = LinearRegression()
    ARRdata = proccesModel[0]
    n_sample = []
    n_feature = []
    for x in range(futureForcast, len(ARRdata)):
        n_sample.append([ARRdata[x][0]])
        n_feature.append(ARRdata[x][3])
    regresModel.fit(n_sample, n_feature)

    # loop list
    n_result = {'SumPerChg': [], 'predicted': [],
                'FutureChg': [], 'accuracy': []}

    for countARRdata in range(0, len(ARRdata)):
        predicted = regresModel.predict([[ARRdata[countARRdata][0]]])[0]
        n_result['predicted'].append(predicted)
        n_result['SumPerChg'].append(ARRdata[countARRdata][0])
        n_result['FutureChg'].append(ARRdata[countARRdata][3])
        try:
            n_result['accuracy'].append(
                float(predicted)/float(ARRdata[countARRdata][3]))
        except:
            n_result['accuracy'].append(None)

    # print(pd.DataFrame(n_result))
    # for x in range(futureForcast):
    #     n_result['accuracy'].remove(None)

    # print("\n",({'coefficient': regresModel.coef_[0], 'intercept':regresModel.intercept_}))
    predictedPrice = APIdata(tickerNum)[
        0]+(n_result['predicted'][0]/100*APIdata(tickerNum)[0])
    for x in n_result['accuracy']:
        if x == None:
            n_result['accuracy'].remove(None)
    # print(" accuracy: ", np.round(np.average(n_result['accuracy']), 2), " predictedPrice: ", predictedPrice )
    return {'predictedChg': n_result['predicted'][0], 'predictedPrice': predictedPrice}

# fig, axs = plt.subplots(2)

# axs[0].plot(n_result['accuracy'])
# axs[0].set_title("accuracy")
# axs[1].plot(n_result['predicted'])
# axs[1].plot(n_result['FutureChg'])
# plt.show()


# plt.show()
