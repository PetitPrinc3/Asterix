import subprocess

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
subprocess.run('cp -r /var/lib/docker/volumes/DataShare/_data/user_inp.json /var/lib/docker/volumes/DataShare/_data/trt_result.json', shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)


subprocess.run("su - docker_runner -c '/usr/bin/docker exec -w /usr/share/USBHandler -it backend python3 main.py'", shell = True)
subprocess.run("/var/dev/USBOutputPart", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
subprocess.run("umount /dev/USBOutputDisk", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
info('You can now remove the USB output drive.')


with spinner('Waiting for drive removal...'):
    ud.rem_wait(["/dev/USBInputDisk", "/dev/USBInputPart"])
success('Done. Thank you for using IMOTEP <3')
