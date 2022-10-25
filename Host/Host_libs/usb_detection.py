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
            time.sleep(1)
        except KeyboardInterrupt:
            print()
            return None
    success('::: USB device detected :::          ')
    return path[[os.path.exists(_) for _ in path].index(True)]


################################################################################


def rem_wait(path):
    while True in [_ in os.listdir(os.path.join(_.split("/"))) for _ in path]:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print()
            return False
    fail('::: USB device removed  :::          ')
    return True


################################################################################
