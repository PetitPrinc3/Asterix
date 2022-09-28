#!/usr/bin/python3

import subprocess
from spinner import spinner
from prints import *

print("""
____________________________
___       ___          
\  \ \**\ \  \    ##    /**/
 \  \ \**\ \  \  ##   /**/
 /  / /**/ /  /   ##   \**\
/__/ /**/ /__/   ###    \**\
____________________________

""")

if subprocess.run('whoami', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8').strip() != 'root': fail('This program must be run as root.'); exit()

def get_docker():
    with spinner('Installing Docker Engine...'):
        subprocess.call("curl -fsSL https://get.docker.com -o get-docker.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        info('Fetched install script.        ')
        subprocess.call("bash get-docker.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        info('Docker installed.              ')
        subprocess.call("rm get-docker.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("docker version", shell=True)
    success('Docker Engine installed.')

def cmd_run(cmd):
    if subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0: fail('Process failed. This is critical.'); fail("Exiting now."); exit()

if subprocess.run('docker version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stderr.decode('utf-8').strip() == '/bin/sh: 1: docker: not found': warning('Oops, docker is not installed. Installing now !'); get_docker()

with spinner('Creating source folders...'):
    cmd_run("/usr/bin/mkdir /src")
    cmd_run("/usr/bin/rm -r /src/*")
    cmd_run("/usr/bin/mdir /dev/Frontend")
    cmd_run("/usr/bin/mdir /dev/Backend")
success("Source folders created.")


with spinner('Creating software users'):
    if subprocess.run('su fdp', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stderr.decode('utf-8').strip() == 'su: user docker_runner does not exist or the user entry does not contain all the required fields':
        cmd_run("useradd -m -d /opt/docker_runner docker_runner")
    cmd_run("usermod -aG docker docker_runner")
success('Software users created.')


with spinner('Preparing Frontend software...'):
    cmd_run("/usr/bin/cp -r Frontend /src/Frontend")
    cmd_run("/usr/bin/chown -R docker_runner:docker /src/Frontend")
success("Frontend software prepared.")


with spinner('Preparing Backend software...'):
    cmd_run("/usr/bin/cp -r Backend /src/Backend")
    cmd_run("/usr/bin/chown -R docker_runner:docker /src/Backend")
success("Backend software retrieved.")


with spinner('Collecting PyRATE...'):
    cmd_run("/usr/bin/git clone https://github.com/G4vr0ch3/PyRATE /src/Frontend/PyRATE")
success("Pyrate collected.")


with spinner('Collecting PyRATE automation wrapper...'):
    cmd_run("/usr/bin/git clone https://github.com/G4vr0ch3/PyrateAutomation /src/Frontend/PyrateAutomation")
success("Pyrate automation wrapper collected.")


with spinner('Collecting USB input detection software...'):
    cmd_run("/usr/bin/git clone https://github.com/G4vr0ch3/USBInputDetection /src/USBInputDetection")
    cmd_run("/usr/bin/cp -r /src/USBInputDetection/Frontend/PythonHandler /src/Frontend/USBInputDetection")
    cmd_run("/usr/bin/cp -r /src/USBInputDetection/Backend/PythonHandler /src/Backend/USBInputDetection")
success("USB input detection software collected.")


with spinner('Adding UDEV rules...'):
    cmd_run("/usr/bin/cp /src/USBInputDetection/Frontend/00-frontend.rules /etc/udev/rules.d")
    cmd_run("/usr/bin/cp /src/USBInputDetection/Backend/00-backend.rules /etc/udev/rules.d")
    info('Reloading rules...')
    cmd_run("udevadm control --reload-rules")
    info('Triggering rules...')
    cmd_run("udevadm trigger")
success("UDEV rules added.")


info("Building Frontend container...")
cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker build -t frontend /src/Frontend"', shell=True)
success("Frontend software installed.")

info("Building Backend container...")
cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker build -t backend /src/Backend"', shell=True)
success("Backend software installed.")


with spinner('Creating relevant docker volumes...'):
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name InputFiles"', shell=True)
    info('InputFiles volume created')
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name OutputFiles"', shell=True)
    info('OutputFiles volume created')
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name SharedDB"', shell=True)
    info('SharedDB volume created')
success("All relevant docker volumes created.")


with spinner('Creating USB UIDs database...'):
    cmd_run("/usr/bin/python3 db_create.py")
    cmd_run("/usr/bin/mv USB_ID.db /var/lib/docker/volumes/SharedDB/_data")
success("USB UIDs database initialized.")


with spinner('Starting containers...'):
    cmd_run("/usr/bin/cp boot.sh /opt/docker_runner/boot.sh")
    cmd_run("/usr/bin/cp boot.sh /opt/docker_runner/run.sh")
    cmd_run('/usr/bin/su - docker_runner -c "/bin/bash /opt/docker_runner/boot.sh"', shell=True)
success("Docker containers started.")


info('Preparing Windows 10 VM Environment...')
cmd_run("/usr/bin/mkdir /src/win10_VM")
cmd_run("/usr/bin/cp /usr/share/AAVMF/AAVMF_CODE.fd /src/win10_VM/AAVMF_CODE.fd")
cmd_run("/usr/bin/cp /usr/share/AAVMF/AAVMF_VARS.fd /src/win10_VM/AAVMF_VARS.fd")

with spinner('Creating system disk image...'):
    cmd_run("/usr/bin/qemu-img create -f vhdx -o subformat=fixed /src/win10_VM/system.vhdx 64G")
success('64Gb System disk image was initialized.')


with spinner('Collecting VirtIO drivers...'):
    cmd_run("/usr/bin/curl https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/virtio-win-0.1.221-1/virtio-win-0.1.221.iso -o /src/win10-VM/virtio_drivers.iso", shell=True)
success('VirtIO drivers collected.')

with spinner('Collecting windows UUID...'):
    UUID=cmd_run("""/usr/bin/wget --no-check-certificate -qO- "https://uupdump.net/known.php?q=windows+10+21h2+arm64" | grep 'href="\./selectlang\.php?id=.*"' -o | sed 's/^.*id=//g' | sed 's/"$//g' | head -n1""", shell=True)
    WIN_LANG="en-us"
success('Collected windows UUID.')

with spinner('Collected windows downloader from UUPdump...'):
    cmd_run('/usr/bin/mkdir tmp', shell=True)
    cmd_run(f'/usr/bin/wget --no-check-certificate -O "tmp/uupdump.zip" "https://uupdump.net/get.php?id={UUID}&pack={WIN_LANG}&edition=professional&autodl=2"', shell=True)
    cmd_run('/usr/bin/unzip -q "tmp/uupdump.zip"', shell=True)
success('Collected windows downloader.')

info('Downloading windows ISO. This will take some time.')
cmd_run("tmp/uup_download_linux.sh", shell=True)
success('Windows ISO collected.')


with spinner('Finalizing VM environment...'):
    cmd_run("/usr/bin/mv tmp/*.ISO /src/win10_VM")
success("VM environment finalized")

cmd_run("/usr/bin/rm -r tmp", shell=True)

info("""When you are ready to setup the VM, execute "bash vm_setup.sh". Follow the instructions provided on the repository's README.""")

# SETUP END
success("Exhausted")