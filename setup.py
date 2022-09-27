#!/usr/bin/python3

import subprocess
from spinner import spinner
from prints import *

if subprocess.run('whoami', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8').strip() != 'root': fail('This program must be run as root.'); exit()

with spinner('Creating source folders...'):
    subprocess.call("/usr/bin/mkdir /src", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("/usr/bin/mdir /dev/Frontend", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("/usr/bin/mdir /dev/Backend", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success("Source folders created.")


with spinner('Adding UDEV rules...'):
    subprocess.call("/usr/bin/cp 00-frontend.rules /etc/udev/rules.d", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("/usr/bin/cp 00-backend.rules /etc/udev/rules.d", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    info('Reloading rules...')
    subprocess.call("udevadm control --reload-rules", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    info('Triggering rules...')
    subprocess.call("udevadm trigger", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success("UDEV rules added.")


with spinner('Downloading Frontend software...'):
    subprocess.call("/usr/bin/git clone https://github.com/G4vr0ch3/Frontend /src/Frontend", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("/usr/bin/chown -R docker_runner:docker /src/Frontend", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("/usr/bin/chmod +x /src/Frontend/setup.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success("Frontend software retrieved.")


with spinner('Downloading Backend software...'):
    subprocess.call("/usr/bin/git clone https://github.com/G4vr0ch3/Backend /src/Backend", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("/usr/bin/chown -R docker_runner:docker /src/Backend", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("/usr/bin/chmod +x /src/Backend/setup.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success("Backend software retrieved.")


with spinner('Installing Frontend Software, this may take some time...'):
    subprocess.call("/src/Frontend/setup.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success("Frontend software installed.")

with spinner('Installing Backend Software, this may take some time...'):
    subprocess.call("/src/Backend/setup.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success("Backend software installed.")


with spinner('Creating relevant docker volumes...'):
    subprocess.call('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name InputFiles"', shell=True)
    info('InputFiles volume created')
    subprocess.call('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name OutputFiles"', shell=True)
    info('OutputFiles volume created')
    subprocess.call('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name SharedDB"', shell=True)
    info('SharedDB volume created')
success("All relevant docker volumes created.")


with spinner('Creating USB UIDs database...'):
    subprocess.call("/usr/bin/python3 db_create.py", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("/usr/bin/mv USB_ID.db /var/lib/docker/volumes/SharedDB/_data", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success("USB UIDs database initialized.")


with spinner('Starting containers...'):
    subprocess.call("/usr/bin/cp boot.sh /opt/docker_runner/boot.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("/usr/bin/cp boot.sh /opt/docker_runner/run.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call('/usr/bin/su - docker_runner -c "/bin/bash /opt/docker_runner/boot.sh"', shell=True)
success("Docker containers started.")

# SETUP END
success("Exhausted")