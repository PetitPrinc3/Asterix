#!/usr/bin/python3.10


################################################################################


import os

from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner


################################################################################


def format(drive):

#    try:
#        os.system(f'umount {drive}')
#    except:
#        fail('Un-mount opperation failed.')
#        return False

    try:
        with spinner(f'Formating {drive}'):
            os.system(f'mkfs.vfat {drive}')
        
        success('Drive formatting succeeded.')
    except:
        fail('Drive formatting failed.')
        return False

    return True


################################################################################
