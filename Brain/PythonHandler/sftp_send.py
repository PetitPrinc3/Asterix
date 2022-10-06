import subprocess
import paramiko
import json
import os

from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner

target ='127.0.0.1'
username = 'ac-center'
password = 'ac-center'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

with spinner('Establishing connection with AC-Center...'):

    client.connect(target, port=10022, username=username, password=password)
    sftp = client.open_sftp()
        
success('Connected to AC-Center.')

subprocess.run("/usr/bin/cp /mnt/DataShare/user_inp.json user_inp.json")

with open("user_inp.json", "r") as inp:
    js_data = json.load(inp)["ind_results"]

info('Begining file transfer to AC-Center.')
fail = False
ind_results = []

for file in js_data:

    inp = file["filename"]
    outp = f'/Users/ac-center/Desktop/PywavaAutomation/PyWAVA/Inputs/{os.path.basename(inp)}'

    with spinner(f'Sending file {inp} to AC-Center'):
        try:
            sftp.put(inp, outp)

            ind_result = {
                "Date": file["Date"],
                "FileName": outp,
                "HASH": file["Hash"]
            }

            ind_results.append(ind_result)

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

    sftp.put("inputs.json", f'/Users/ac-center/Desktop/PywavaAutomation/')

    success('Inputs initialized.')

except:
    fail("Failed to write transfer results.")