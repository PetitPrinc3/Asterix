#!/usr/bin/python3.10


################################################################################


import json

import init_json as ij
import runs_pywava as rp
import fetch_results as fr
import cleaner as cl

from Asterix_libs import log
from Asterix_libs.prints import *
from datetime import datetime


################################################################################


start = datetime.now()

log.log('BEGINING OF ANALYSIS PROCESS.')

print()

# Initialize environment
info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Initializing environment.')
ij.init_res('Pywava\scan_results.json')

print()

info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Cleaning Pywava folders.')
cl.clean_fold('Pywava\Inputs')
log.log('Cleaned Pywava\Inputs')

print()

info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Fetching inputs.')
lst = rp.getlist('inputs.json')
fls = rp.move(lst, 'Pywava\Inputs')

print()

# Run Pyrate
info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Attempting analyses.')
rp.runs_(fls)

print()

# Get results
info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Fetching results')

ij.init_res('clean.json')

res = fr.get_stats('Pywava\scan_results.json')

with open('clean.json', 'r+') as outp:

    log.log('Opened clean.json')

    files = []

    for suc in res[0]:
        success(f'File {suc["PATH"]} is clean.')
        files.append(suc)

    js = json.load(outp)

    js['ind_results'] = files

    outp.seek(0)

    js = json.dumps(js, indent = 4)

    outp.write(js)

log.log('Closed clean.json')

print()

for fai in res[1]:
    fail(f'File {fai["PATH"]} is malicious.')

end = datetime.now()

elapsed = end-start

print()

info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Exhausted in ' + str(elapsed))
log.log('END OF ANALYSIS PROCESS.')


################################################################################
