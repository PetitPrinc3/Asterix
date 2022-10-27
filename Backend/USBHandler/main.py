#!/usr/bin/python3.10
################################################################################


import subprocess
import json

import usb_detection as ud
import usb_id as uid
import usb_list as ul
import usb_format as uf
import Asterix_libs.copy as cp

from Asterix_libs.spinner import spinner
from Asterix_libs.prints import *
from Asterix_libs.log import *


################################################################################


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

    reset_log("backendMAINlog.txt")

    subprocess.call('/bin/cp /mnt/DataShare/trt_result.json trt_result.json', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        with open("trt_result.json", "r") as res:
            js_res = json.load(res)
            if len(js_res["ind_result"]) == 0:
                warning('Nothing to export.')
                log('Nothing to export', "backendMAINlog.txt")
                export_log("backendMAINlog.txt")
                return 1
    
    except:
        warning('Nothing to export.')
        log('Nothing to export', "backendMAINlog.txt")
        export_log("backendMAINlog.txt")
        return 1


    if not uid.db_test("/mnt/DataShare/USB_ID.db"): log("DB Test failed.", "backendMAINlog.txt"); exit()

    outp = ud.inp_wait(["/mnt/USBOutputDevice/USBOutputPart", "/mnt/DataShare/BadUSBOutput"])

    if outp is None: fail('Output detection failed.'); log("Output Detection BUG ***", "backendMAINlog.txt") ;export_log("backendMAINlog.txt"); exit()
    if outp == "/mnt/DataShare/BadUSBOutput": fail("The output drive is not a valid USB drive."); log("BAD OUTPUT DEVICE ***", "backendMAINlog.txt"); subprocess.call("rm -f /mnt/DataShare/BadUSBOutput", shell=True); fail('This incident will be reported.'); exit()

    parts = []
    
    for _ in os.listdir("/mnt/USBOutputDevice/USBOutputPart"):
        
        if os.path.isdir(f"/mnt/USBOutputDevice/USBOutputPart/{_}"):
            parts.append(_)  

    n_part = len(parts)

    log(f"Found {n_part} partitions. ({parts})","backendMAINlog.txt")

    if n_part > 1:

        try:
            print(' ' + '_'*(len(str(len(parts))) + max([len(part) for part in parts]) + 5))

            for part in parts:
                print('| ' + '0'*(len(str(len(parts))) - len(str(parts.index(part)))) + str(parts.index(part)) + ' | ' + part + ' '*(max([len(part) for part in parts]) - len(part)) + ' |')

            print('|_' + "_"*(len(str(len(parts)))) + '_|_' + '_'*max(len(part) for part in parts) + '_|')

            info(f'Found {n_part} partitions. Select the partition that Asterix should use :')

            while True:

                try:
                    choice = int(input('>>> '))

                    if choice >= len(parts):
                        warning('Choose an existing partition.')

                    else:
                        s_part = "/mnt/USBOutputDevice/USBOutputPart/" + parts[choice]
                        log(f"Selected partition {s_part}.", "backendMAINlog.txt")
                        break

                except KeyboardInterrupt:

                    fail('Choice failed.')
                    log("Stopped at partition selection.", "backendMAINlog.txt")
                    export_log("backendMAINlog.txt")
                    exit()

                except:

                    warning('Choice failed. The choice has to be made by partition index (eg: 0). Try again.')

        except:

            print(parts, n_part)

    else:

        s_part = "/mnt/USBOutputDevice/USBOutputPart/" + os.listdir("/mnt/USBOutputDevice/USBOutputPart")[0]


    Vid, Pid = uid.get_ids("/dev/" + s_part.split("/")[-1])

    log(f'Detected USB drive with Vid: {Vid} and Pid: {Pid}.', "backendMAINlog.txt")

    val = uid.match_ids("/mnt/DataShare/USB_ID.db", Vid, Pid)

    if not val: 
        log("Vid/Pid do NOT match.", "backendMAINlog.txt")
        fail('Output device not recognized.') 
        print("Vendor ID  : ", Vid)
        print("Product ID : ", Pid)
        
        # print("Do you want to format the drive and use it anyway ? (Y/n)")
        # ch = str(input('>>> '))
        # if ch == 'Y':
        #     print()
        #     warning('This operation is definitive. The drive contains the following files :')
        #     tab(ul.lst(outp))
        #     print('Confirm (Y/n)')
        #     ch = str(input('>>> '))
        #     if ch == 'Y':
        #         print()
        #         uf.format(outp)
        #     else:
        #         fail("USB Identification failed. Exiting.")
        #         exit()
        # else:
        #     fail("USB Identification failed. Exiting.")
        #     exit()

        fail("USB Identification failed. Exiting.")
        export_log("backendMAINlog.txt")
        exit()

    else:
        success('Output Device recognized !')
        log("Pid/Vid MATCH.", "backendMAINlog.txt")

    print()


    with open("trt_result.json", "r") as res:
        f_trt = [f["FileName"] for f in json.load(res)["ind_results"]]

    f_res = cp.xcopy("trt_result.json", f_trt, s_part)

    print("\nAvailable Files :")
    
    t_lst = [_[35:] for _ in f_res]
    tab(t_lst)

    log(f'Final copied files : {f_res}', "backendMAINlog.txt")

    export_log("backendMAINlog.txt")


if __name__ == "__main__":
    main()


################################################################################
