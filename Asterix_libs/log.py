#!/usr/bin/python3.10


################################################################################


import subprocess
from datetime import datetime


################################################################################


def init_log(path=""):

    if path[-1] != "/": path += "/"

    time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    name = path + f'[{time}]-logfile.txt'

    with open(name, "w") as logfile:
        logfile.write(f'[{time}] - Initialized log file.')

    return name


def reset_log(file="log.txt"):
    time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    with open(file, "w") as logfile:
        logfile.write(f'[{time}] - Initialized log file.')


def log(data, file="log.txt"):  

    time = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    line = f'[{time}] - {data}'

    with open(file, "r+") as l_file:

        logs = l_file.read()

        logs = line + '\n' + logs

        l_file.seek(0)

        l_file.write(logs)


def log_from_log(local_log, global_log):

    local_log_entries = open(local_log, "r").readlines()

    with open(global_log, "r+") as gl:

        global_log_entries = gl.readlines() + local_log_entries

        gl.seek(0)

        gl.writelines(global_log_entries)


def export_log(fpath):
    subprocess.call(f'mv {fpath} /mnt/DataShare/', shell=True)

################################################################################
