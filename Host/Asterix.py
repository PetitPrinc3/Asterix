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
subprocess.run("""systemctl stop inppartmnt@$(udevadm info -q all -a /dev/USBInputPart | grep KERNEL | head -n 1 | cut -d '"' -f 2).service""" , shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
subprocess.run("""systemctl stop inpdiskmnt@$(udevadm info -q all -a /dev/USBInputDisk | grep KERNEL | head -n 1 | cut -d '"' -f 2).service""" , shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
info('You can now remove the USB input drive.')


subprocess.run("su - docker_runner -c '/usr/bin/docker exec -w /usr/share/PythonHandler -it brain python3 main.py'", shell = True)

subprocess.run("su - docker_runner -c '/usr/bin/docker exec -w /usr/share/PyrateAutomation -it frontend python3 main.py'", shell = True)

subprocess.run("su - docker_runner -c '/usr/bin/docker exec -w /usr/share/USBHandler -it backend python3 main.py'", shell = True)
info('You can now remove the USB output drive.')
subprocess.run("""systemctl stop outpartmnt@$(udevadm info -q all -a /dev/USBOutputPart | grep KERNEL | head -n 1 | cut -d '"' -f 2).service""" , shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
subprocess.run("""systemctl stop outdiskmnt@$(udevadm info -q all -a /dev/USBOutputDisk | grep KERNEL | head -n 1 | cut -d '"' -f 2).service""" , shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

with spinner('Waiting for drive removal...'):
    ud.rem_wait(["/dev/USBInputDisk", "/dev/USBInputPart", "/dev/USBOutputDisk", "/dev/USBOutputPart"])
success('Done. Thank you for using Asterix <3')
