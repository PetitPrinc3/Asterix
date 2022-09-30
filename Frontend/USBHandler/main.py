#!/usr/bin/python3.10


################################################################################


import subprocess

import usb_detection as ud
import usb_list as ul
import copy as cp

from Asterix_libs.prints import *


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

        print(' ' + "_"*((max((ct//10), 2)) + colsize + 5))
        print('| ID ' + " "*(max((ct//10) - 2, 0)) + "| File " + " "*(colsize - 4) + "|")

        for f in f_lst:
            print('| ' + "0"*max(((ct//10) - f_lst.index(f)//10), 1) + str(f_lst.index(f)) + " | " + str(f)[-colsize:] + " "*(colsize - len(f[-colsize:])) + " |")

        print('|' + "_"*((max((ct//10), 2)) + colsize + 5) + '|\n')

def main():
    inp = ud.inp_wait("/dev/USBInputPart", "/dev/USBInputDisk")

    if inp is None : fail('Input detection failed.'); exit()

    subprocess.run(f'mount {inp} /mnt/USBInputDevice', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    f_lst = ul.lst('/mnt/USBInputDevice')

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

    print("\nAvailable Files :")
    tab(f_res)

    subprocess.run(f'umount {inp}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    main()


################################################################################
