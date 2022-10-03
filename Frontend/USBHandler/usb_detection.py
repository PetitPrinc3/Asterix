#!/usr/bin/python3.10


################################################################################


import os
import time

from datetime import datetime
from Asterix_libs.prints import *


################################################################################


def inp_wait(path):
    while True not in [os.path.exists(_) for _ in path]:
        try:
            infor('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Waiting for USB Device')
            time.sleep(1)
        except KeyboardInterrupt:
            print()
            return None
    return path[[os.path.exists(_) for _ in path].index(True)]


################################################################################


def rem_wait(path):
    while True in [os.path.exists(_) for _ in path]:
        try:
            infor('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Waiting for USB Device')
            time.sleep(1)
        except KeyboardInterrupt:
            print()
            return False
    fail('::: USB device removed  :::          ')
    return True


################################################################################
