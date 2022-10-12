#!/usr/bin/python3.10


################################################################################


import subprocess
from datetime import datetime


################################################################################


def init_log(path=""):

    if len(path) > 0 and path[-1] != "/": path += "/"

    time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    name = path + f'[{time}]-logfile.txt'

    with open(name, "w") as logfile:
        logfile.write(f'[{time}] - Initialized log file.')

    return name


def reset_log(file="log.txt"):
    time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    with open(file, "w") as logfile:
        logfile.write(f'[{time}] - Initialized log file.')
    return file


def log(data, file="log.txt"):  

    time = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    line = f'[{time}] - {data}'

    with open(file, "r+") as l_file:

        logs = l_file.read()

        logs = logs + '\n' + line

        l_file.seek(0)

        l_file.write(logs)


def log_from_log(local_log, global_log):

    local_log_entries = open(local_log, "r").read()
    global_log_entries = open(global_log, "r").read()

    with open(global_log, "w") as gl:

        entries = global_log_entries + '\n' + local_log_entries

        gl.write(entries)


def export_log(fpath):
    subprocess.call(f'/bin/mv {fpath} /mnt/DataShare/', shell=True)
    subprocess.call(f'/bin/chmod +r /mnt/DataShare/{fpath.split("/")[-1]}', shell=True)


################################################################################
