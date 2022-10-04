#!/usr/bin/python3

import subprocess
import os
from Asterix_libs.spinner import spinner
from Asterix_libs.prints import *


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
    if subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() != 0: fail('Process failed. This is critical.'); print(cmd); fail("Exiting now."); exit()


if subprocess.run('docker version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stderr.decode('utf-8').strip() == '/bin/sh: 1: docker: not found': warning('Oops, docker is not installed. Installing now !'); get_docker()


if subprocess.Popen('qemu-system-aarch64 -machine help', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() != 0: 
    with spinner('Collecting QEMU KVM...'):
        cmd_run("apt install virt-manager libvirt0 qemu-system -y")
    success('QEMU KVM Installed.')

with spinner('Creating source folders...'):
    if not os.path.exists("/src"): cmd_run("/usr/bin/mkdir /src")
    if len(os.listdir("/src")) != 0: cmd_run("/usr/bin/rm -r /src/*")
success("Source folders created.")


with spinner('Creating software users'):
    if subprocess.Popen('id docker_runner', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() != 0:
        cmd_run("/usr/sbin/useradd -m -d /opt/docker_runner docker_runner")
    cmd_run("/usr/sbin/usermod -aG docker docker_runner")
success('Software users created.')


with spinner('Preparing Frontend software...'):
    cmd_run("/usr/bin/cp -r Frontend /src/Frontend")
    cmd_run("/usr/bin/cp -r Asterix_libs /src/Frontend")
    cmd_run("/usr/bin/chown -R docker_runner:docker /src/Frontend")
success("Frontend software prepared.")


with spinner('Preparing Backend software...'):
    cmd_run("/usr/bin/cp -r Backend /src/Backend")
    cmd_run("/usr/bin/cp -r Asterix_libs /src/Backend")
    cmd_run("/usr/bin/chown -R docker_runner:docker /src/Backend")
success("Backend software retrieved.")


with spinner('Collecting PyRATE...'):
    cmd_run("/usr/bin/git clone https://github.com/G4vr0ch3/PyRATE /src/Frontend/PyRATE")
success("Pyrate collected.")


with spinner('Adding mounting service...'):
    cmd_run('mkdir -p /usr/share/Asterix/Mounters')
    cmd_run('/usr/bin/cp Host/Mounters/*.sh /usr/share/Asterix/')
    cmd_run('/usr/bin/cp Host/Mounters/*.service /etc/systemd/system/')
    cmd_run('systemctl daemon-reload')
success('Created mounting service.')


with spinner('Adding UDEV rules...'):
    cmd_run("/usr/bin/cp Host/00-frontend.rules /etc/udev/rules.d")
    cmd_run("/usr/bin/cp Host/00-backend.rules /etc/udev/rules.d")
    info('Reloading rules...      ')
    cmd_run("udevadm control --reload-rules")
    info('Triggering rules...     ')
    cmd_run("udevadm trigger")
success("UDEV rules added.")


with spinner("Building Frontend container. This may take some time..."):
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker build -t frontend /src/Frontend"')
success("Frontend software installed.")


with spinner("Building Backend container. This may take some time..."):
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker build -t backend /src/Backend"')
success("Backend software installed.")


with spinner('Creating relevant docker volumes...'): 
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name USBInputDevice"')
    info('USBInputDevice volume created.        ')
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name InputFiles"')
    info('InputFiles volume created.             ')
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name USBOutputDevice"')
    info('USBOutputDevice volume created.       ')
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name OutputFiles"')
    info('OutputFiles volume created.            ')
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name DataShare"')
    info('DataShare volume created.              ')
success("All relevant docker volumes created.")


with spinner('Starting containers...'):
    cmd_run("/usr/bin/cp Host/docker_runner_scripts/boot.sh /opt/docker_runner/boot.sh")
    cmd_run("/usr/bin/cp Host/docker_runner_scripts/run.sh /opt/docker_runner/run.sh")
    subprocess.run('/usr/bin/su - docker_runner -c "/bin/bash /opt/docker_runner/boot.sh"', shell=True)
success("Docker containers started.")


# info('Preparing Windows 10 VM Environment...')
# cmd_run("/usr/bin/mkdir /src/win10_VM")
# cmd_run("/usr/bin/cp /usr/share/AAVMF/AAVMF_CODE.fd /src/win10_VM/AAVMF_CODE.fd")
# cmd_run("/usr/bin/cp /usr/share/AAVMF/AAVMF_VARS.fd /src/win10_VM/AAVMF_VARS.fd")


# with spinner('Creating system disk image...'):
#     cmd_run("/usr/bin/qemu-img create -f vhdx -o subformat=fixed /src/win10_VM/system.vhdx 64G")
# success('64Gb System disk image was initialized.')


# info('Collecting VirtIO drivers...')
# subprocess.Popen("/usr/bin/wget --no-check-certificate -O /src/win10_VM/virtio_drivers.iso https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/virtio-win-0.1.221-1/virtio-win-0.1.221.iso", shell=True)
# success('VirtIO drivers collected.')

# with spinner('Collecting windows UUID...'):
#     UUID=subprocess.Popen("""/usr/bin/wget --no-check-certificate -qO- "https://uupdump.net/known.php?q=windows+10+21h2+arm64" | grep 'href="\./selectlang\.php?id=.*"' -o | sed 's/^.*id=//g' | sed 's/"$//g' | head -n1""", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
#     WIN_LANG="en-us"
# success('Collected windows UUID.')


# info('Collected windows downloader from UUPdump...')
# cmd_run('/usr/bin/mkdir tmp')
# subprocess.run(f'/usr/bin/wget --no-check-certificate -O "tmp/uupdump.zip" "https://uupdump.net/get.php?id={UUID}&pack={WIN_LANG}&edition=professional&autodl=2"', shell=True)
# cmd_run('cd tmp && /usr/bin/unzip -q "uupdump.zip"')
# success('Collected windows downloader.')

# info('Downloading windows ISO. This will take some time.')
# subprocess.run("cd tmp && /bin/bash uup_download_linux.sh", shell=True)
# success('Windows ISO collected.')


# with spinner('Finalizing VM environment...'):
#     cmd_run("/usr/bin/mv tmp/*.ISO /src/win10_VM")
# success("VM environment finalized")

# cmd_run("/usr/bin/rm -r tmp")


# info("""When you are ready to setup the VM, execute "bash vm_setup.sh". Follow the instructions provided on the repository's README.""")

# SETUP END
success("Exhausted")