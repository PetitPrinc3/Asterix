#!/usr/bin/python3.10


################################################################################


from datetime import datetime


################################################################################


def log(data):

    time = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    line = f'[{time}] - {data}'

    with open("log.txt", "r+") as l_file:

        logs = l_file.read()

        logs = line + '\n' + logs

        l_file.seek(0)

        l_file.write(logs)


################################################################################
