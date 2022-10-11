#!/usr/bin/python3.10


################################################################################


from datetime import datetime


################################################################################


def init_log():

    time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    name = f'[{time}]-logfile.txt'

    with open(name, "w") as logfile:
        logfile.write(f'[{time}]Initialized log file.')

def log(data):  

    time = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    line = f'[{time}] - {data}'

    with open("log.txt", "r+") as l_file:

        logs = l_file.read()

        logs = line + '\n' + logs

        l_file.seek(0)

        l_file.write(logs)


################################################################################
