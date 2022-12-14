#!/usr/bin/python3.10
################################################################################


import subprocess
import time
import os
import json

import usb_detection as ud
import usb_list as ul

import Asterix_libs.copy as cp

from datetime import datetime
from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner
from Asterix_libs.hash import sha
from Asterix_libs.log import *


################################################################################


def choose():
    return [int(c) for c in str(input(">>> ")).split(";")]

def tab(f_lst):
    if f_lst == []:
        print(" ____________________ ")
        print("| No File Available. |")
        print("|____________________|")
        print()
    
    else:
        ct = len(f_lst)
        colsize = min(max([len(path) for path in f_lst]), 200)
        print(' ' + "_"*(len(str(ct//10)) + colsize + 6) + ' ')
        print('| ID' + " "*(max(len(str(ct//10)), 0)) + "| File " + " "*(colsize - 4) + "|")
        print('|'+"_"*(len(str(ct//10)) + 3) + "|" + "_"*(colsize + 2) + "|")
        for f in f_lst:
            if f_lst.index(f) < 10: ifinf=1
            else: ifinf=0
            print('| ' + "0"*max(len(str(ct//10)) - len(str(f_lst.index(f)//10)) + ifinf, 0) + str(f_lst.index(f)) + " | " + str(f)[-colsize:] + " "*(colsize - len(f[-colsize:])) + " |")

        print('|'+"_"*(len(str(ct//10)) + 3) + "|" + "_"*(colsize + 2) + "|\n")

def main():

    reset_log("frontMAINlog.txt")

    inp = ud.inp_wait(["/mnt/USBInputDevice/USBInputPart", "/mnt/DataShare/BadUSBInput"])

    log("USB Input detected.","frontMAINlog.txt")

    if inp is None : fail('Input detection failed.'); export_log("frontMAINlog.txt"); exit()
    if inp == "/mnt/DataShare/BadUSBInput": fail("The input drive is not a valid USB drive."); subprocess.call("rm -f /mnt/DataShare/BadUSBInput", shell=True); fail('This incident will be reported.'); log("BAD USB INPUT IDENTIFIED.","frontMAINlog.txt"); export_log("frontMAINlog.txt"); exit()

    success('::: USB device detected :::          ')

    log("Mass storage unit detected.","frontMAINlog.txt")

    time.sleep(1)

    parts = []
    for _ in os.listdir("/mnt/USBInputDevice/USBInputPart"):
        
        if os.path.isdir(f"/mnt/USBInputDevice/USBInputPart/{_}"):
            parts.append(_)  

    n_part = len(parts)

    info(f'Found {n_part} partitions.')
    log(f"Found {n_part} partitions. ({parts})","frontMAINlog.txt")

    if n_part > 1:

        try:
            print(' ' + '_'*(len(str(len(parts))) + max([len(part) for part in parts]) + 5))

            for part in parts:
                print('| ' + '0'*(len(str(len(parts))) - len(str(parts.index(part)))) + str(parts.index(part)) + ' | ' + part + ' '*(max([len(part) for part in parts]) - len(part)) + ' |')

            print('|_' + '_'*(len(str(len(parts)))) + '_|_' + '_'*max(len(part) for part in parts) + '_|')

            print('Select the partition that Asterix should use :')

            while True:

                try:
                    choice = int(input('>>> '))

                    if choice >= len(parts):
                        warning('Choose an existing partition.')

                    else:
                        s_part = "/mnt/USBInputDevice/USBInputPart/" + parts[choice]
                        log(f"Selected partition {s_part}.", "frontMAINlog.txt")
                        break

                except KeyboardInterrupt:

                    fail('Choice failed.')
                    log("Stopped at partition selection.", "frontMAINlog.txt")
                    export_log("frontMAINlog.txt")
                    exit()

                except:

                    warning('Choice failed. The choice has to be made by partition index (eg: 0). Try again.')

        except:

            print(parts, n_part)

    else:

        s_part = "/mnt/USBInputDevice/USBInputPart/" + os.listdir("/mnt/USBInputDevice/USBInputPart")[0]

    tmout = 0

    subprocess.call('cp default.json list_result.json', shell=True)

    with spinner("Collecting input drive content..."):
        while True:
            if tmout > 7 or len(os.listdir(s_part))>0:
                f_lst = ul.lst(s_part)
                break
            else:
                time.sleep(1)
                tmout += 1


    info('Fetched ' + str(len(f_lst)) + ' files.')
    
    t_lst = [_[33:] for _ in f_lst]
    tab(t_lst)
    
    log("The following files were found : " + str(f_lst),"frontMAINlog.txt")

    if f_lst == []: warning("No file available on input drive. Exiting."); subprocess.call("cp default.json /mnt/DataShare/user_inp.json", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); export_log("frontMAINlog.txt"); exit()
    
    print("Select files by ID (Separate your choice with ';'. e.g '1;2;3') :")
    
    while True:
        
        try:
            choice = choose()
            break

        except KeyboardInterrupt:
            fail(KeyboardInterrupt)
            export_log("frontMAINlog.txt")
            exit()

        except:
            fail('Choice failed, try again.')

    f_trt = []
    for ind in choice:
        f_trt.append(f_lst[ind])
    
    print("\nSelected Files :")
    
    t_lst = [_[33:] for _ in f_trt]
    tab(t_lst)
    
    f_res = cp.xcopy("list_result.json", f_trt, "/mnt/InputFiles/")

    log("The following files were selected : " + str(f_trt), "frontMAINlog.txt")
    log("Validated files : " + str(f_res), "frontMAINlog.txt")

    print()

    print('Do you wish to perform a fast scan or a complete scan ? (f/c) :')

    while True:

        try:
            choice = str(input('>>> '))[0].lower()
            if choice == 'f':
                stype = 'FASTSCAN'
                log("Scan type chosen : FAST", "frontMAINlog.txt")
                break
            elif choice == 'c':
                stype = 'COMPLETESCAN'
                log("Scan type chosen : COMPLETE", "frontMAINlog.txt")
                break
            else:
                fail('Choice failed, try again.')

        except KeyboardInterrupt:
            fail(KeyboardInterrupt)
            exit()

        except:
            fail('Choice failed, try again.')

    subprocess.call("cp default.json /mnt/DataShare/user_inp.json", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open('/mnt/DataShare/user_inp.json', 'r+') as usr_fl:

        f_data = json.load(usr_fl)

        for file in f_res:

            ind_result = {
                "Date": datetime.now().strftime("%d/%m/%Y-%H:%M:%S"),
                "FileName": file,
                "HASH": sha(file),
                "SCANTYPE": stype
            }

            f_data["ind_results"].append(ind_result)
    
            log("File " + str(file) + " : " + str(ind_result), "frontMAINlog.txt")

        usr_fl.seek(0)
        js = json.dumps(f_data, indent=4)
        usr_fl.write(js)

    print("\nAvailable Files :")

    t_lst = [_[16:] for _ in f_res]
    tab(t_lst)

    export_log("frontMAINlog.txt")

    

if __name__ == "__main__":
    main()


################################################################################