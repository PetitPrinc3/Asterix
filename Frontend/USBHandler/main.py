#!/usr/bin/python3.10
################################################################################


import subprocess
import time
import json

import usb_detection as ud
import usb_list as ul
import copy as cp

from datetime import datetime
from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner
from Asterix_libs.hash import sha


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
    inp = ud.inp_wait(["/mnt/USBInputDevice/USBInputPart", "/mnt/USBInputDevice/USBInputDisk", "/mnt/DataShare/BadUSBInput"])

    if inp is None : fail('Input detection failed.'); exit()
    if inp == "/mnt/DataShare/BadUSBInput": fail("The input drive is not a valid USB drive."); subprocess.call("rm /mnt/DataShare/BadUSBInput", shell=True); fail('This incident will be reported.'); exit()

    success('::: USB device detected :::          ')

    with spinner("Collecting input drive content..."):
        time.sleep(1)
        f_lst = ul.lst(inp)
    info('Fetched ' + str(len(f_lst)) + ' files.')
    
    tab(f_lst)
    if f_lst == []: warning("No file available on input drive. Exiting."); exit()
    print("Select files by ID (Separate your choice with ';'. e.g '1;2;3') :")
    while True:
        try:
            choice = choose()
            break
        except KeyboardInterrupt:
            fail(KeyboardInterrupt)
            exit()
        except:
            fail('Choice failed, try again.')
    f_trt = []
    for ind in choice:
        f_trt.append(f_lst[ind])
    print("\nSelected Files :")
    tab(f_trt)
    f_res = cp.xcopy("list_result.json", f_trt, "/mnt/InputFiles/")

    with open('/mnt/DataShare/user_inp.json', 'r+') as usr_fl:

        f_data = json.load(usr_fl)

        for file in f_res:


            ind_result = {
                "Date": datetime.now().strftime("%d/%m/%Y-%H:%M:%S"),
                "FilePath": file,
                "HASH": sha(file),
            }

            f_data["ind_results"].append(ind_result)

        usr_fl.seek(0)
        js = json.dumps(f_data, indent=4)
        usr_fl.write(js)

    print("\nAvailable Files :")
    tab(f_res)

if __name__ == "__main__":
    main()


################################################################################