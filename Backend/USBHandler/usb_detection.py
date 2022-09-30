#!/usr/bin/python3.10


################################################################################


import os
import time

from datetime import datetime
from prints import *


################################################################################


def inp_wait(path1, path2="$"):
    while not os.path.exists(path1) and not os.path.exists(path2):
        try:
            infor('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Waiting for Output Device')
            time.sleep(1)
        except KeyboardInterrupt:
            print()
            return None
    success('::: Output device detected :::          ')
    if os.path.exists(path1): return path1
    if os.path.exists(path2): return path2


################################################################################


def rem_wait(path1, path2="$"):
    while os.path.exists(path1) or os.path.exists(path2):
        try:
            infor('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Waiting for Output Device')
            time.sleep(1)
        except KeyboardInterrupt:
            print()
            return False
    fail('::: Output device removed  :::          ')
    return True


################################################################################
