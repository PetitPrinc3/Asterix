#!/usr/bin/python3.10


################################################################################


import os
import sys
import json
import paramiko
import subprocess


import cleaner as cl
import init_json as ij
import runs_pywava as rp
import fetch_results as fr

from Asterix_libs import log
from datetime import datetime
from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner


################################################################################


target ='127.0.0.1'
port = 10022
username = 'ac-center'
password = 'ac-center'


start = datetime.now()


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


log.log('BEGINING OF ANALYSIS PROCESS.')


with spinner('Establishing connection with AC-Center...'):

    client.connect(target, port=10022, username=username, password=password)
    transport = client.get_transport()

    if transport.is_active():
        try:
            transport.send_ignore()
        except Exception as _e:
            fail('SSH Connection failed.')
            sys.exit(1)
    else:
        fail('SSH Connection failed.')
        
success('Connected to AC-Center.')


with spinner('Establishing SFTP connection with AC-Center...'):

    sftp = client.open_sftp()
        
success('SFTP Session opened.')


with spinner('Establishing RCE channel with AC-Center...'):

    transport = client.get_transport()
    channel = transport.open_session()
    c, r = os.get_terminal_size(0)
    channel.get_pty(width=int(c))
        
success('RCE channel opened.')


print()


# Initialize environment
info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Initializing environment.')
ij.init_res(sftp, '\\Users\\ac-center\\Desktop\\PywavaAutomation\\Pywava\\scan_results.json')


print()


info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Cleaning Pywava folders.')
cl.clean_fold(channel, '\\Users\\ac-center\\Desktop\\PywavaAutomation\\Pywava\\Inputs')
log.log('Cleaned Pywava\Inputs')


print()


subprocess.run("/bin/cp /mnt/DataShare/user_inp.json user_inp.json", shell = True)

with open("user_inp.json", "r") as inp:
    js_data = json.load(inp)["ind_results"]

info('Begining file transfer to AC-Center.')
fail = False
ind_results = []

for file in js_data:

    inp = file["FileName"]
    outp = f'/Users/ac-center/Desktop/PywavaAutomation/PyWAVA/Inputs/{os.path.basename(inp)}'

    with spinner(f'Sending file {inp} to AC-Center'):
        try:
            sftp.put(inp, outp)

            ind_results.append(file)

            success(f'File {inp} was successfully transfered to AC-Center')
        except:
            fail = True
            fail(f'File {inp} could not be transfered.')

if fail == True: warning('Some files were not transfered.')
else: info('All selected files were transfered')

try:
    with open("inputs.json", "w") as inp:
        
        js_base = {
                'ind_results': ind_results
            }

        inp.seek(0)

        js_inp = json.dumps(js_base, indent=4)

        inp.write(js_inp)

    success('Inputs initialized.')

except:
    fail("Failed to write transfer results.")

print()

# Run Pyrate
info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Attempting analyses.')

channel.shutdown_write()

rp.runs_(channel, "inputs.json")

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
