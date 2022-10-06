#!/usr/bin/python3.10


################################################################################


import json
import paramiko

import os

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


def runs_(channel, json):

    files = json.load(json)["ind_results"]

    for file in files:
        print()

        if file["SCANTYPE"] == "FASTSCAN": channel.exec_command(f'cd C:\\Users\\ac-center\\Desktop\\PywavaAutomation\\PyWAVA && python pywava.py -b -d -f C:\\Users\\ac-center\\Desktop\\PywavaAutomation\\PyWAVA\\Inputs\\{os.path.basename(file["FileName"])}')
        if file["SCANTYPE"] == "COMPLETESCAN": channel.exec_command(f'cd C:\\Users\\ac-center\\Desktop\\PywavaAutomation\\PyWAVA && python pywava.py -b -cd -f C:\\Users\\ac-center\\Desktop\\PywavaAutomation\\PyWAVA\\Inputs\\{os.path.basename(file["FileName"])}')

        log.log(f'System call : "cd Pywava && python pywava.py -b -cd -f {os.getcwd()}\Pywava\Inputs\{os.path.basename(file[1])}"')


################################################################################
