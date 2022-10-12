#!/usr/bin/python3.10


################################################################################


import os
import sys
import json
import paramiko
import subprocess


import PywavaAutomation.runs_pywava as rp
import PywavaAutomation.fetch_results as fr


from Asterix_libs.log import *
from datetime import datetime
from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner


################################################################################


target ='127.0.0.1'
port = 10022
username = 'ac-center'
password = 'ac-center'


def ac_run():

    start = datetime.now()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    log('BEGINING OF ANALYSIS PROCESS.', "PywavaAutomation/pywavalog.txt")


    with spinner('Establishing connection with AC-Center...'):

        client.connect(target, port=10022, username=username, password=password)
        transport = client.get_transport()
        c, r = os.get_terminal_size(0)


        if transport.is_active():
            try:
                transport.send_ignore()
            except Exception as _e:
                fail('SSH Connection failed.')
                log('SSH Connection with AC-CENTER failed.', "PywavaAutomation/pywavalog.txt")
                sys.exit(1)
        else:
            fail('SSH Connection failed.')
            log('SSH Connection with AC-CENTER failed.', "PywavaAutomation/pywavalog.txt")
            sys.exit(1)

            
    success('Connected to AC-Center.')
    log('SSH Connection with AC-CENTER established.', "PywavaAutomation/pywavalog.txt")


    print()


    # Initialize environment
    info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Initializing environment.')
    sftp = client.open_sftp()
    log('SFTP Connection with AC-CENTER established. (SCANRESULTSINIT)', "PywavaAutomation/pywavalog.txt")
    sftp.put("default.json", '\\Users\\ac-center\\Desktop\\PywavaAutomation\\Pywava\\scan_results.json')

    print()


    info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Cleaning Pywava folders.')

    channel = transport.open_session()
    log('RCE Connection with AC-CENTER established.', "PywavaAutomation/pywavalog.txt")
    channel.get_pty(width=int(c))
    channel.exec_command('python \\Users\\ac-center\\Desktop\\PywavaAutomation\\Pywava\\clean_inputs_fold.py')

    with spinner("Cleaning Input folder..."):
        while True:
            if channel.exit_status_ready():
                break

    log('Cleaned Pywava input folder.', "PywavaAutomation/pywavalog.txt")

    print()


    subprocess.run("/bin/cp /mnt/DataShare/user_inp.json user_inp.json", shell = True)


    with open("user_inp.json", "r") as inp:
        js_data = json.load(inp)["ind_results"]


    info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Begining file transfer to AC-Center.')
    fl = False
    ind_results = []

    log('Transfering files to AC Center.', "PywavaAutomation/pywavalog.txt")

    for file in js_data:

        inp = file["FileName"]
        outp = f'\\Users\\ac-center\\Desktop\\PywavaAutomation\\PyWAVA\\Inputs\\{os.path.basename(inp)}'

        with spinner(f'Sending file {inp} to AC-Center'):
            try:

                sftp = client.open_sftp()
                sftp.put(inp, outp, confirm=True)

                ind_results.append(file)

                success(f'File {inp} was successfully transfered to AC-Center')
                log(f'File {inp} was successfully transfered to AC-Center', "PywavaAutomation/pywavalog.txt")
            except:
                fl = True
                fl(f'File {inp} could not be transfered.')
                log(f'File {inp} could not be transfered.', "PywavaAutomation/pywavalog.txt")


    if fl == True: warning('Some files were not transfered.')
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
        log('Inputs initialized.', "PywavaAutomation/pywavalog.txt")

    except:
        fail("Failed to write transfer results.")
        log('Failed to write transfer results.', "PywavaAutomation/pywavalog.txt")

    print()

    # Run PyWAVA
    info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Attempting analyses.')

    log('Runing analyses.', "PywavaAutomation/pywavalog.txt")
    rp.runs_(transport, "inputs.json", c)
    log('Done with analyses.', "PywavaAutomation/pywavalog.txt")

    print()
    
    # Get results
    info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Fetching results')

    log('Retrieving analyses results.', "PywavaAutomation/pywavalog.txt")
    sftp.get('\\Users\\ac-center\\Desktop\\PywavaAutomation\\Pywava\\scan_results.json', 'scan_results.json')

    res = fr.get_stats('scan_results.json')

    end = datetime.now()

    elapsed = end-start

    print()

    info('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Exhausted in ' + str(elapsed))

    try:
        subprocess.call("/bin/cp clean.json /mnt/DataShare/clean.json", shell = True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

    log('END OF ANALYSIS PROCESS.')

    return res


################################################################################
