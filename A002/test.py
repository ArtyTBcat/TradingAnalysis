# import numpy as np
# mylist = [11, 18, 19, 21, 10 ,11, 12, 13, 14]
# interval = 5

# patternlist = []
# for x in range(len(mylist)):
#     newlist = []
#     for y in range(interval):
#         newlist.append(mylist[x+y])
#     patternlist.append(str(newlist))
#     print(patternlist)



# newPattern = []
# newChange = []
# for x in range(len(var['pattern'])):
#     patternTempo = []
#     changeTempo = []
#     for y in range(interval):
#         patternTempo.append(var['pattern'][x+y])
#         changeTempo.append(var['change'][x+y])
#     newPattern.append(str(patternTempo))
#     newChange.append(str(changeTempo))
# var['pattern'] = newPattern
# var['change'] = newChange



import subprocess
from datetime import datetime
import time

while True:
    if  '00' <= datetime.now().strftime("%M") <= '05' or '30' <= datetime.now().strftime("%M") <= '35':
        subprocess.call("A002-03.py", shell=True)
    time.sleep(60)

    




