#!/usr/bin/python3.10


################################################################################


import os
import sys
import json
import paramiko
import subprocess


from Asterix_libs import hash
from Asterix_libs import log
from Asterix_libs.prints import *


################################################################################


devnull = open(os.devnull, 'w')


def getlist(json_file):

    f, _ = [], []

    with open(json_file, 'r') as targets:

        log.log(f'Opened {json_file}')
        js = json.load(targets)

        for target in js['files']:

            f_name = target['FileName']
            f_path = target['FilePath']
            f_hash = target['HASH']

            while f_name.split(".")[0] in [_[0] for _ in f]:

                f_name = f_name.split(".")[0] + '_.' + f_name.split(".")[-1]

            _.append([f_name, f_path, f_hash])

    log.log(f'Closed {json_file}')
    log.log(f'Retrieved file lst : {_}')

    return _


################################################################################


def move(f, folder_out):

    stat, f_ = [], []

    for file in f:
        subprocess.call(f'copy {file[1]} {folder_out}\{file[0]}', shell = True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log.log(f'System call : "move {file[1]} {folder_out}\{file[0]}"')
        file[1] = f'{folder_out}\{file[0]}'

    for file in f:
            try:
                if hash.sha(f'{folder_out}\{file[0]}') == file[2]:
                    stat.append(True)
                    success(f'{file[0]} copied successfully.')
                else:
                    stat.append(False)
                    fail(f'{file[0]} was not copied successfully.')
            except:
                fail(f'{file[0]} was not copied successfully.')

    for res in range(len(stat)):
        if stat[res] == True: f_.append(f[res])

    log.log(f'Got {f_}')

    return f_


################################################################################


def runs_(transport, jsonfile, c):

    with open(jsonfile, "r") as inst:
        files = json.load(inst)["ind_results"]

    for file in files:
        print()

        channel = transport.open_session()
        channel.get_pty(width=int(c))

        if file["SCANTYPE"] == "FASTSCAN":
            channel.exec_command(f'cd \\Users\\ac-center\\PyWAVA && python pywava.py -b -d -f "\\Users\\ac-center\\PyWAVA\\Inputs\\{os.path.basename(file["FileName"])}"')
        if file["SCANTYPE"] == "COMPLETESCAN": 
            channel.exec_command(f'cd \\Users\\ac-center\\PyWAVA && python pywava.py -b -cd -f "\\Users\\ac-center\\PyWAVA\\Inputs\\{os.path.basename(file["FileName"])}"')

        while not channel.recv_ready():
            pass

        channel.recv(15).decode('utf-8')

        while True:

            try:

                if channel.recv_ready():
                    sys.stdout.write(channel.recv(4096).decode('utf-8'))

                if channel.exit_status_ready():
                    sys.stdout.write(channel.recv(4096).decode('utf-8'))
                    break

            except KeyboardInterrupt:
                fail('Operation terminated by user Keyboard Interrupt.')
                break


################################################################################
