import subprocess
import json

from datetime import datetime

from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner

from Host_libs import usb_detection as ud

from Host_libs.db_create import create

subprocess.run('rm -r /var/lib/docker/volumes/InputFiles/_data/* /var/lib/docker/volumes/OutputFiles/_data/* /var/lib/docker/volumes/DataShare/_data/*', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

create()

subprocess.run('cp USB_ID.db /var/lib/docker/volumes/DataShare/_data/', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run("su - docker_runner -c '/usr/bin/docker exec -w /usr/share/USBHandler -it frontend python3 main.py'", shell = True)
subprocess.run("umount /var/lib/docker/volumes/USBInputDevice/_data/USBInputPart", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
subprocess.run("umount /var/lib/docker/volumes/USBInputDevice/_data/USBInputDisk", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
info('You can now remove the USB input drive.')

subprocess.run('cp -r /var/lib/docker/volumes/InputFiles/_data/* /var/lib/docker/volumes/OutputFiles/_data/*', shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

subprocess.run('cp ../Brain/default.json /var/lib/docker/volumes/DataShare/_data/trt_result.json')

with open("/var/lib/docker/volumes/DataShare/_data/trt_result.json", "r+") as out:

    jsout = json.load(out)

    with open("/var/lib/docker/volumes/DataShare/_data/user_inp.json", "r") as inp:
    
        jsinp = json.load(inp)

        for js in jsinp["ind_results"]:
            
            ind_result = {
                "Date": datetime.now().strftime("%d/%m/%Y-%H:%M:%S"),
                "FileName": "/mnt/OutFiles/" + js["FileName"].split('/mnt/InputFiles')[-1],
                "HASH": js["HASH"]
            }

            jsout["ind_results"].append(ind_result)

    out.seek(0)
    jsfi = json.dumps(jsout, indent=4)
    out.write(jsfi)

subprocess.run("su - docker_runner -c '/usr/bin/docker exec -w /usr/share/USBHandler -it backend python3 main.py'", shell = True)
subprocess.run("/var/dev/USBOutputPart", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
subprocess.run("umount /dev/USBOutputDisk", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
info('You can now remove the USB output drive.')


with spinner('Waiting for drive removal...'):
    ud.rem_wait(["/dev/USBInputDisk", "/dev/USBInputPart"])
success('Done. Thank you for using IMOTEP <3')
