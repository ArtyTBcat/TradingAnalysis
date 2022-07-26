import subprocess
from datetime import datetime
import time

while True:
    if  '00' <= datetime.now().strftime("%M") <= '05' or '30' <= datetime.now().strftime("%M") <= '35':
        subprocess.call("A002-03.py", shell=True)
    time.sleep(60)