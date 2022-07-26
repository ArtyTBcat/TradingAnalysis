import pandas
from A005_01.A005_01 import main as A005Main
from A004_copy.A004_01 import main as A004Main
from datetime import datetime
import time

df = []

while True:
    predict = datetime.now().strftime("%H:%M:%S"), A004Main(0)
    print(predict)
    df.append(predict)
    time.sleep(60*5)
    if datetime.now().strftime("%H") == "10":
        a_dataframe = pandas.DataFrame(df)
        a_dataframe.to_pickle("predictionValues.plk")
        output = pandas.read_pickle("predictionValues.plk")
        print("\n", output)
        break

# print(A005Main())
