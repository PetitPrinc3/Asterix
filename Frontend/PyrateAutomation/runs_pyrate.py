#!/usr/bin/python3.10


################################################################################


import os
import json
import subprocess
from Asterix_libs import hash
from Asterix_libs import log

from Asterix_libs.prints import *


################################################################################


def getlist(json_file):

    f, _ = [], []

    with open(json_file, 'r') as targets:

        log.log(f'Opened {json_file}')
        js = json.load(targets)

        for target in js['ind_results']:

            f_path = target['FileName']
            f_name = os.path.basename(f_path)
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
        subprocess.call(f'cp {file[1]} {folder_out}/{file[0]}', shell = True)
        log.log(f'System call : "cp {file[1]} {folder_out}/{file[0]}"')
        file[1] = f'{folder_out}/{file[0]}'

    for file in f:
            try:
                if hash.sha(f'{folder_out}/{file[0]}') == file[2]:
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


def runs_(f):

    for file in f:
        subprocess.call(f'cd Pyrate; ./pyrate.py -b -f {file[1].split("Pyrate/")[-1]}', shell = True)
        log.log(f'System call : "cd Pyrate; ./pyrate.py -b -f {file[1].split("Pyrate/")[-1]}"')


################################################################################
