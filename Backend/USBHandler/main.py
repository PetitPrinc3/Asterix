#!/usr/bin/python3.10
################################################################################


import subprocess

import usb_detection as ud
import copy as cp
import usb_id as uid
import usb_list as ul
import usb_format as uf
from Asterix_libs.spinner import spinner
from Asterix_libs.prints import *


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

    if not uid.db_test("/mnt/DataShare/USB_ID.db"): exit()

    cp.copy("/mnt/DataShare/trt_result.json", "trt_result.json")

    outp = ud.inp_wait(["/mnt/USBOutputDevice/USBOutputPart", "/mnt/USBOutputDevice/USBOutputDisk", "/mnt/DataShare/BadUSBOutput"])

    if outp is None: fail('Output detection failed.'); exit()
    if outp == "/mnt/DataShare/BadUSBOutput": fail("The output drive is not a valid USB drive."); subprocess.call("rm /mnt/DataShare/BadUSBOutput", shell=True); fail('This incident will be reported.'); exit()

    Vid, Pid = uid.get_ids("/dev/" + outp.split("/")[-1])

    val = uid.match_ids("/mnt/DataShare/USB_ID.db", Vid, Pid)

    if not val: 
        fail('Output device not recognized.') 
        print("Vendor ID  : ", Vid)
        print("Product ID : ", Pid)
        print("Do you want to format the drive and use it anyway ? (Y/n)")
        ch = str(input('>>> '))
        if ch == 'Y':
            print()
            warning('This operation is definitive. The drive contains the following files :')
#            subprocess.run(f'mount {outp} /mnt/USBOutputDevice', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            tab(ul.lst(outp))
#            subprocess.run(f'umount {outp}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print('Confirm (Y/n)')
            ch = str(input('>>> '))
            if ch == 'Y':
                print()
                uf.format(outp)
            else:
                fail("USB Identification failed. Exiting.")
                exit()
        else:
            fail("USB Identification failed. Exiting.")
            exit()
    else:
        success('Output Device recognized !')

#    subprocess.run(f'mount {outp} /mnt/USBOutputDevice', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print()

    f_trt = ul.lst('/mnt/OutputFiles')

    f_res = cp.xcopy("trt_result.json", f_trt, outp)
    
    print("\nAvailable Files :")
    tab(f_res)
#    subprocess.run('umount /mnt/USBOutputDevice', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    info('You can now remove the USB output drive.')

    ud.rem_wait([outp])

    success('Done. Thank you for using IMOTEP <3')


if __name__ == "__main__":
    main()


################################################################################
