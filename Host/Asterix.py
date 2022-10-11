import subprocess
import json

from datetime import datetime

from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner

from Host_libs import usb_detection as ud
from Host_libs.db_create import create

from pyfiglet import figlet_format as pfg


print(pfg('Asterix'))

subprocess.run('rm -r /var/lib/docker/volumes/InputFiles/_data/* /var/lib/docker/volumes/OutputFiles/_data/* /var/lib/docker/volumes/DataShare/_data/*', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

create()

subprocess.run('/usr/bin/sudo -u root /usr/bin/python /src/Host/db_create.py', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/USBHandler -it frontend python3 main.py", shell = True)

subprocess.run("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/PythonHandler -it brain python3 main.py", shell = True)

subprocess.run("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/PyrateAutomation -it frontend python3 main.py", shell = True)

subprocess.run("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/PythonHandler -it brain python3 gen_res.py", shell = True)

subprocess.run("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/USBHandler -it backend python3 main.py", shell = True)

subprocess.run("/usr/bin/sudo -u root /bin/bash /src/Host/eject_devices.sh", shell = True)

info('You can now remove both USB drives.')

with spinner('Waiting for drive removal...'):
    ud.rem_wait(["/dev/USBInputDisk", "/dev/USBInputPart", "/dev/USBOutputDisk", "/dev/USBOutputPart"])
success('Done. Thank you for using Asterix <3')
