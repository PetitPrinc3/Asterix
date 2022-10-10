#!/usr/bin/python3.10


################################################################################


import json
import subprocess

import init_json as ij
import runs_pyrate as rp
import fetch_results as fr
import cleaner as cl

from Asterix_libs.prints import *
from Asterix_libs import log
from datetime import datetime


################################################################################


subprocess.call("/bin/cp /mnt/DataShare/dirty.json inputs.json", shell = True)

with open("inputs.json", "r") as inp:
    js = json.load(inp)
    if len(js["ind_results"]) == 0:
        subprocess.call('/bin/cp default.json /mnt/DataShare/san_clean.json', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        exit()

start = datetime.now()

log.log('BEGINING OF SANITIZING PROCESS.')

print()

# Initialize environment
info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Initializing environment.')
ij.init_res('Pyrate/san_results.json')

print()

info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Cleaning Pyrate folders.')
cl.clean_fold('Pyrate/Inputs')
log.log('Cleaned Pyrate/Inputs')
cl.clean_fold('Pyrate/Outputs')
log.log('Cleaned Pyrate/Outputs')


print()

info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Fetching inputs.')
lst = rp.getlist('inputs.json')
fls = rp.move(lst, 'Pyrate/Inputs')

print()

# Run Pyrate
info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Attempting sanitizing operations.')
rp.runs_(fls)

print()

# Get results
info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Fetching results')

ij.init_res('clean.json')

res = fr.get_stats('Pyrate/san_results.json')

subprocess.call('/bin/cp default.json san_clean.json', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

with open('san_clean.json', 'r+') as outp:

    log.log('Opened san_clean.json')

    files = []

    if len(res[0]) > 0:

        for suc in res[0]:

            subprocess.call(f'/bin/cp Pyrate/{suc["OUTPATH"]} /mnt/Sanitized/{suc["FileName"]}')

            success(f'File {suc["FileName"]} was sanitized succesfully.')
            
            file_ = {
                "Date": suc["Date"],
                "FileName": f'/mnt/Sanatized/{suc["FileName"]}',
                "HASH": suc["HASH"]
            }

            files.append(file_)

        js = json.load(outp)

        js['ind_results'] = files

        outp.seek(0)

        js = json.dumps(js, indent = 4)

        outp.write(js)

log.log('Closed san_clean.json')

print()

for fai in res[1]:
    fail(f'File {fai["FileName"]} couls not be sanitized.')

end = datetime.now()

elapsed = end-start

subprocess.call('/bin/cp san_clean.json /mnt/DataShare/san_clean.json', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print()

info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Exhausted in ' + str(elapsed))
log.log('END OF SANITIZING PROCESS.')


################################################################################
