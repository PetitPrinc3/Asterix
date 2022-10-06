import json
import subprocess

from Asterix_libs.prints import *

from PywavaAutomation import pywavaautomation

subprocess.call("/usr/bin/rm dirty.json", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

ac_res = pywavaautomation.ac_run()

subprocess.call("/bin/cp default.json clean.json", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

with open('clean.json', 'r+') as outp:

    files = []

    for suc in ac_res[0]:
        success(f'File {suc["PATH"]} is clean.')
        files.append(suc)

    js = json.load(outp)

    js['ind_results'] = files

    outp.seek(0)

    js = json.dumps(js, indent = 4)

    outp.write(js)

print()

if len(ac_res[1]) > 0:

    subprocess.call("/bin/cp default.json dirty.json", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    for fai in ac_res[1]:
        fail(f'File {fai["PATH"]} were flagged as malicious.')

    print()
    print("Do you wish to try and sanitize the files ? (Y/n)")

    while True:
        choice = str(input('>>> '))[0].lower()

        if choice == 'y':
            san = True
            break

        elif choice == 'n':
            san = False
            break

        else:
            fail('Choice failed, try again.')

subprocess.call("/bin/cp clean.json /mnt/DataShare/trt_results.json", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

