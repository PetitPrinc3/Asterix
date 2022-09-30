#!/usr/bin/python3.10

import subprocess

import usb_detection as ud
import copy as cp
import usb_id as uid
import usb_list as ul
import usb_format as uf
from spinner import spinner

from prints import *


def tab(f_lst):

    if f_lst == []:
        print(" ____________________ ")
        print("| No File Available. |")
        print("|____________________|")
        print()
    
    else:
        ct = len(f_lst)

        colsize = min(max([len(path) for path in f_lst]), 200)

        print(' ' + "_"*((max((ct//10), 2)) + colsize + 5))
        print('| ID ' + " "*(max((ct//10) - 2, 0)) + "| File " + " "*(colsize - 4) + "|")

        for f in f_lst:
            print('| ' + "0"*max(((ct//10) - f_lst.index(f)//10), 1) + str(f_lst.index(f)) + " | " + str(f)[-colsize:] + " "*(colsize - len(f[-colsize:])) + " |")

        print('|' + "_"*((max((ct//10), 2)) + colsize + 5) + '|\n')


def main():
    
    if not uid.db_test("/mnt/SharedDB/USB_ID.db"): exit()

    cp.copy("/mnt/OutputFiles/trt_result.json", "trt_result.json")

    outp = ud.inp_wait("/dev/USBOutputPart", "/dev/USBOutputDisk")

    if outp is None: fail('Output detection failed.'); exit()

    print()
    Vid, Pid = uid.get_ids(outp)

    val = uid.match_ids("/mnt/SharedDB/USB_ID.db", Vid, Pid)

    if not val: 
        fail('Output device not recognized.') 
        print("Vendor ID  : ", Vid)
        print("Product ID : ", Pid)
        print("Do you want to format the drive and use it anyway ? (Y/n)")
        ch = str(input('>>> '))
        if ch == 'Y':
            print()
            warning('This operation is definitive. The drive contains the following files :')
            subprocess.run(f'mount {outp} /mnt/USBOutputDevice', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            tab(ul.lst("/mnt/USBOutputDevice"))
            subprocess.run(f'umount {outp}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
    
    subprocess.run(f'mount {outp} /mnt/USBOutputDevice', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    f_trt = ul.lst('/mnt/OutputFiles')

    f_res = cp.xcopy("trt_result.json", f_trt, "/mnt/USBOutputDevice/")

    print("\nAvailable Files :")
    tab(f_res)

    subprocess.run('umount /mnt/USBOutputDevice', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    info('You can now remove the USB output drive.')

    ud.rem_wait(outp)

    success('Done. Thank you for using IMOTEP <3')


if __name__ == "__main__":
    main()