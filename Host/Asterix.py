import subprocess

from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner
from Asterix_libs.log import *

from Host_libs import usb_detection as ud

from pyfiglet import figlet_format as pfg


try:

    print(pfg('Asterix'))

    subprocess.run("/usr/bin/mkdir -p /opt/asterix/.tmp/", shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)

    logfile = init_log()

    log("Asterix started.", logfile)


    if subprocess.Popen("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/PythonHandler -it brain /bin/sh init_clean.sh", shell = True).wait() != 0:log("Failed to clean shared folders.", logfile); exit()
    log("Cleaned shared folders.", logfile)


    if subprocess.Popen("/usr/bin/sudo -u root /usr/bin/cp /src/Host/Administration/USB_ID.db /var/lib/docker/volumes/DataShare/_data/USB_ID.db", shell = True).wait() != 0:log('Failed to copy database to shared folders.', logfile); exit()
    log("Copied database to shared folders.", logfile)


    if subprocess.Popen("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/USBHandler -it frontend python3 main.py", shell = True).wait() != 0:log('Failed to execute frontend - main.')


    if subprocess.Popen('sudo -u root /usr/bin/cp /var/lib/docker/volumes/DataShare/_data/frontMAINlog.txt /opt/asterix/.tmp/', shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL).wait() != 0:log('Failed to export logs frontend - main.', logfile); exit()
    else:log_from_log('/opt/asterix/.tmp/frontMAINlog.txt', logfile)

    if subprocess.Popen("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/PythonHandler -it brain python3 main.py", shell = True).wait() != 0:log('Failed to execute brain - main.', logfile); exit()

    if subprocess.Popen('sudo -u root /usr/bin/cp /var/lib/docker/volumes/DataShare/_data/brainMAINlog.txt /opt/asterix/.tmp/', shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL).wait() != 0:log('Failed to export logs brain - main.', logfile); exit()
    log_from_log('/opt/asterix/.tmp/brainMAINlog.txt', logfile)

    if subprocess.Popen("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/PyrateAutomation -it frontend python3 main.py", shell = True).wait() != 0:log('Failed to execute frontend - pyrate.', logfile); exit()

    if subprocess.Popen('sudo -u root /usr/bin/cp /var/lib/docker/volumes/DataShare/_data/frontPYRATElog.txt /opt/asterix/.tmp/', shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL).wait() != 0:log('Failed to export logs frontend - pyrate.', logfile); exit()
    log_from_log('/opt/asterix/.tmp/frontPYRATElog.txt', logfile)

    if subprocess.Popen("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/PythonHandler -it brain python3 gen_res.py", shell = True).wait() != 0:log('Failed to execute brain - gen_res.', logfile); exit()

    if subprocess.Popen('sudo -u root /usr/bin/cp /var/lib/docker/volumes/DataShare/_data/brainRESlog.txt /opt/asterix/.tmp/', shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL).wait() != 0:log('Failed to export logs brain - gen_res.', logfile); exit()
    log_from_log('/opt/asterix/.tmp/brainRESlog.txt', logfile)

    if subprocess.Popen("/usr/bin/sudo -u docker_runner /usr/bin/docker exec -w /usr/share/USBHandler -it backend python3 main.py", shell = True).wait() != 0:log('Failed to execute backend - main.', logfile); exit()

    if subprocess.Popen('sudo -u root /usr/bin/cp /var/lib/docker/volumes/DataShare/_data/backendMAINlog.txt /opt/asterix/.tmp/', shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL).wait() != 0:log('Failed to export logs backend - main.', logfile); exit()
    log_from_log('/opt/asterix/.tmp/backendMAINlog.txt', logfile)

    if subprocess.Popen("/usr/bin/sudo -u root /bin/bash /src/Host/Host_Scripts/eject_devices.sh", shell = True).wait() != 0:log('Failed to ehject devices.', logfile); exit()

    log("USB Devices ejected.", logfile)

    info('You can now remove both USB drives.')

    with spinner('Waiting for drive removal...'):
        ud.rem_wait(["/dev/USBInputDisk", "/dev/USBInputPart", "/dev/USBOutputDisk", "/dev/USBOutputPart"])
    success('Done. Thank you for using Asterix <3')

    log("USB Devices removed.", logfile)

    log("Asterix completed.", logfile)

except:

    fail('SOMETHING BAD HAPPENED. CRITICAL FAILURE DETECTED. EXITING.')
    try:
        log('CRITICAL FAILURE', logfile)
    except:
        pass