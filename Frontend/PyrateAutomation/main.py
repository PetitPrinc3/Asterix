#!/usr/bin/python3.10


################################################################################


import json
import subprocess

import init_json as ij
import runs_pyrate as rp
import fetch_results as fr
import cleaner as cl

from Asterix_libs.prints import *
from Asterix_libs.log import *
from datetime import datetime


################################################################################


reset_log("frontPYRATElog.txt")

subprocess.call("/bin/cp /mnt/DataShare/dirty.json inputs.json", shell = True)

with open("inputs.json", "r") as inp:
    js = json.load(inp)
    if len(js["ind_results"]) == 0:
        subprocess.call('/bin/cp default.json /mnt/DataShare/san_clean.json', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        exit()

start = datetime.now()

log('BEGINING OF SANITIZING PROCESS.', "frontPYRATElog.txt")

print()

# Initialize environment
info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Initializing environment.')
ij.init_res('Pyrate/san_results.json')

print()

info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Cleaning Pyrate folders.')
cl.clean_fold('Pyrate/Inputs')
log('Cleaned Pyrate/Inputs', "frontPYRATElog.txt")
cl.clean_fold('Pyrate/Outputs')
log('Cleaned Pyrate/Outputs', "frontPYRATElog.txt")

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

    log('Opened san_clean.json', "frontPYRATElog.txt")

    files = []

    if len(res[0]) > 0:

        for suc in res[0]:

            subprocess.call(f'/bin/cp Pyrate/{suc["OUTPATH"]} /mnt/Sanitized/{suc["FileName"]}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            success(f'File {suc["FileName"]} was sanitized succesfully.')
            log(f'File {suc["FileName"]} was sanitized succesfully.', "frontPYRATElog.txt")
            
            file_ = {
                "Date": suc["Date"],
                "FileName": f'/mnt/Sanitized/{suc["FileName"]}',
                "HASH": suc["HASH"]
            }

            files.append(file_)

        js = json.load(outp)

        js['ind_results'] = files

        outp.seek(0)

        js = json.dumps(js, indent = 4)

        outp.write(js)

log('Closed san_clean.json', "frontPYRATElog.txt")

print()

for fai in res[1]:
    fail(f'File {fai["FileName"]} couls not be sanitized.')

end = datetime.now()

elapsed = end-start

subprocess.call('/bin/cp san_clean.json /mnt/DataShare/san_clean.json', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Exhausted in ' + str(elapsed))

print()

log('END OF SANITIZING PROCESS.', "frontPYRATElog.txt")

export_log("frontPYRATElog.txt")


################################################################################
