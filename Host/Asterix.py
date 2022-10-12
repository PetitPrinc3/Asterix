import subprocess

from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner
from Asterix_libs.log import *

from Host_libs import usb_detection as ud

from pyfiglet import figlet_format as pfg

print(pfg('Asterix'))

logfile = init_log()

log("Asterix started.", logfile)

subprocess.run("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/PythonHandler -it brain /bin/sh init_clean.sh", shell = True)

log("Cleaned shared folders.", logfile)

subprocess.run('/usr/bin/sudo -u root /usr/bin/python /src/Host/db_create.py', shell=True)

log_from_log('/opt/asterix/dblog.txt', logfile)

subprocess.run("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/USBHandler -it frontend python3 main.py", shell = True)

log_from_log('/var/lib/docker/volumes/DataShare/_data/frontMAINlog.txt', logfile)

subprocess.run("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/PythonHandler -it brain python3 main.py", shell = True)

log_from_log('/var/lib/docker/volumes/DataShare/_data/brainMAINlog.txt', logfile)

subprocess.run("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/PyrateAutomation -it frontend python3 main.py", shell = True)

log_from_log('/var/lib/docker/volumes/DataShare/_data/frontPYRATElog.txt', logfile)

subprocess.run("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/PythonHandler -it brain python3 gen_res.py", shell = True)

log_from_log('/var/lib/docker/volumes/DataShare/_data/brainRESlog.txt', logfile)

subprocess.run("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/USBHandler -it backend python3 main.py", shell = True)

subprocess.run("/usr/bin/sudo -u root /bin/bash /src/Host/eject_devices.sh", shell = True)

log("USB Devices ejected.", logfile)

info('You can now remove both USB drives.')

with spinner('Waiting for drive removal...'):
    ud.rem_wait(["/dev/USBInputDisk", "/dev/USBInputPart", "/dev/USBOutputDisk", "/dev/USBOutputPart"])
success('Done. Thank you for using Asterix <3')

log("Asterix completed.", logfile)
