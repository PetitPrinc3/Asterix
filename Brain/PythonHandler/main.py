import json
import subprocess

from ffh import ffh

from Asterix_libs.prints import *
from Asterix_libs.log import *

from PywavaAutomation import pywavaautomation


def is_empty(json_file):

    try:
        with open(json_file, "r") as json_data:

            json_ctnt = json.load(json_data)

            ctnt_len = len(json_ctnt["ind_results"])

            if ctnt_len == 0: return True
            else: return False

    except:
        return True


reset_log("brainMAINlog.txt")
reset_log("PywavaAutomation/pywavalog.txt")


subprocess.call("/bin/cp /mnt/DataShare/user_inp.json user_inp.json", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

if is_empty('user_inp.json'): fail('NOFILE AVAILABLE.'); export_log("brainMAINlog.txt"); subprocess.call("/bin/cp dirty.json /mnt/DataShare/dirty.json", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL); subprocess.call("/bin/cp clean.json /mnt/DataShare/clean.json", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL); exit()

ac_res = pywavaautomation.ac_run()

subprocess.call("/bin/cp default.json clean.json", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

log_from_log("PywavaAutomation/pywavalog.txt", "brainMAINlog.txt")

print()

if len(ac_res[0]) > 0:

    with open('clean.json', 'r+') as outp:

        files = []

        for suc in ac_res[0]:
            success(f'File {suc["PATH"]} is clean.')
            log(f'File {suc["PATH"]} is clean.', "brainMAINlog.txt")
            log(suc, "brainMAINlog.txt")
            file = ffh("user_inp.json", suc["HASH"])
            
            files.append(file)

        js = json.load(outp)

        js['ind_results'] = files

        outp.seek(0)

        js = json.dumps(js, indent = 4)

        outp.write(js)

print()

san = False

if len(ac_res[1]) > 0:

    for fai in ac_res[1]:
        fail(f'File {fai["PATH"]} were flagged as malicious.')
        log(f'File {fai["PATH"]} were flagged as malicious.', "brainMAINlog.txt")
        log(fai, "brainMAINlog.txt")

    print()
    print("Do you wish to try and sanitize the files ? (Y/n)")

    while True:
        choice = str(input('>>> '))[0].lower()

        if choice == 'y':
            san = True
            log(f'Chose PYRATE Sanitization', "brainMAINlog.txt")
            break

        elif choice == 'n':
            san = False
            log(f'Chose NO Sanitization', "brainMAINlog.txt")
            print()
            break

        else:
            fail('Choice failed, try again.')


subprocess.call("/bin/cp default.json dirty.json", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

if san:


    with open('dirty.json', 'r+') as outp:
        files = []

        for fai in ac_res[1]:
            file = ffh("user_inp.json", fai["HASH"])
            
            files.append(file)

        js = json.load(outp)

        js['ind_results'] = files

        outp.seek(0)

        js = json.dumps(js, indent = 4)

        outp.write(js)


subprocess.call("/bin/cp dirty.json /mnt/DataShare/dirty.json", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
subprocess.call("/bin/cp clean.json /mnt/DataShare/clean.json", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

export_log("brainMAINlog.txt")