from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
import pandas as pd
from A005_01 import model

def main():
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(5, 2), random_state=1, max_iter=10000)

    n_class = model.ndarray(model.hisClose(0))
    n_sample = n_class[0]
    n_feature = n_class[1]
    n_featureFloat = n_class[3]

    reg = LinearRegression().fit(n_sample, n_featureFloat)
    # print(reg.score(n_sample, n_feature))

    # print(reg.predict(n_class[2]))

    clf.fit(n_sample, n_feature)
    # print(n_class[2])
    regressionPredict = reg.predict(n_class[2])[0]
    # print("neural_net: ", clf.predict(n_class[2])," Regression:", regressionPredict)

    #find presition
    precition = []
    print(pd.DataFrame(n_featureFloat))
    # print(pd.DataFrame(reg.predict(n_sample)))
    print(pd.DataFrame(n_sample))
    plt.scatter(n_sample, n_feature)
    plt.show()
    # for changeArray in n_sample[4]:
    
    #----------------------------------

    latestPrice = model.hisClose(0)[0]
    pricePredict = latestPrice + (latestPrice*regressionPredict/100)
    # print("predicted price: ",pricePredict)
    return {'neural_net': clf.predict(n_class[2])[0], 'Regression': regressionPredict
            , 'predicted': pricePredict}
    


# print(latestPrice)

# import tensorflow as tf
# # use keras API
# model = tf.keras.Sequential()
# ...
# # compile the model

# model.compile(loss='binary_crossentropy')
# history = model.fit(n_sample, n_feature, epochs=100, batch_size=32)
# print(model.predict(n_class[2][0]))
