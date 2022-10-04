import subprocess

from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner

from Host_libs import usb_detection as ud


subprocess.run("su - docker_runner -c '/usr/bin/docker exec -w /usr/share/USBHandler -it -d frontend python3 main.py'", shell = True)
info('You can now remove the USB input drive.')
subprocess.run("umount /var/lib/docker/volumes/USBInputDevice/_data/USBInputPart", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
subprocess.run("umount /var/lib/docker/volumes/USBInputDevice/_data/USBInputDisk", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)


subprocess.run("su - docker_runner -c '/usr/bin/docker exec -w /usr/share/USBHandler -it -d backend python3 main.py'", shell = True)
info('You can now remove the USB output drive.')
subprocess.run("/var/dev/USBOutputPart", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
subprocess.run("umount /dev/USBOutputDisk", shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)


with spinner('Waiting for drive removal...'):
    ud.rem_wait(["/dev/USBInputDisk", "/dev/USBInputPart"])
success('Done. Thank you for using IMOTEP <3')
