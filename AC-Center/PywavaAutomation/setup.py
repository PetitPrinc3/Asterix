#!/usr/bin/python3

import subprocess
import sys
import os

done = False

for i in sys.path:
    if os.path.isdir(i) and i != "": 
        try:
            libs = subprocess.Popen(f'/usr/bin/cp -r Asterix_libs {i}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if libs.wait() == 0: 
                done = True
                print('Libraries added to python path.')
                subprocess.call('/usr/bin/rm -r Asterix_libs', shell = True)
                break
        except:
            pass

if done:
    from Asterix_libs.prints import success
    success('Done !')
else:
    try:
        subprocess.call('/usr/bin/mv Asterix_libs tmp_', shell = True)
        from Asterix_libs.prints import success
        success('Done !')
        subprocess.call('/usr/bin/rm -r tmp_', shell = True)
    except:
        from Asterix_libs.prints import fail
        fail('Setup failed. Did you run setup.py as root ?')