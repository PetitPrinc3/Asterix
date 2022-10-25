#!/usr/bin/python3.10


################################################################################


import os

from time import sleep
from datetime import datetime
from Asterix_libs.prints import *


################################################################################


def inp_wait(path):
    while True not in [os.path.exists(_) for _ in path]:
        try:
            sleep(.1)
        except KeyboardInterrupt:
            print()
            return None
    success('::: USB device detected :::          ')
    return path[[os.path.exists(_) for _ in path].index(True)]


################################################################################


def rem_wait():
    pres = True
    while pres:
        
        sleep(.1)

        try:
            pres = False
            for _ in os.listdir("/dev"):
                if _.startswith("USBInputPart") or _.startswith("USBOutputPart"):
                    pres = True

        except KeyboardInterrupt:
            fail('Keyboard Interrupt detected.')
            exit(1)

    warning('::: USB devices removed  :::          ')
    return True


################################################################################
