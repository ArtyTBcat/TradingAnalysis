import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# Initialize communication with TMP102
# This function is called periodically from FuncAnimation

import yfinance as yf
end = datetime.datetime.today()
for x in range(30):
    start = end - datetime.timedelta(30)
    historical = yf.download("BTC-USD", start=start,
                             end=end, interval="1h")
    end = end - datetime.timedelta(1)
    print(end)


# plt.axis([0, 1000, 0, 1])

i = 0
x = list()
y = list()

while True:
    while i < 50:
        temp_y = np.random.random()
        x.append(i)
        y.append(temp_y)
        plt.scatter(i, temp_y)
        i += 1
        plt.pause(0.0001)  # Note this correction


def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    temp_c = np.random.randint(10)

    # Add x and y to lists
    xs.append(datetime.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(temp_c)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=90, ha='right')
    plt.title('TMP102 Temperature over Time')
    plt.ylabel('Temperature (deg C)')


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()
