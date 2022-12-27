import yfinance as yf
import datetime

period, interval = "1mo", "1h"
signals = [buy, neutral, sell] = [0, 0.5, 1]


historical = yf.download("BTC-USD", period= period, interval=interval)

# end = datetime.datetime.today()
# for x in range(30):
#     start = end - datetime.timedelta(30)
#     historical = yf.download("BTC-USD", start=start,
#                              end=end, interval="1h")
#     end = end - datetime.timedelta(1)
# historical = yf.download("BTC-USD", start="2022-9-25", end="2022-10-25" ,interval=interval)


print(historical)
print("downloading historical data...")

