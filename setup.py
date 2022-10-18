#!/usr/bin/python3

import subprocess
import sys
import os

from re import sub
from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner


def cmd_run(cmd):
    if subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() != 0: fail('Process failed. This is critical.'); print(cmd); fail("Exiting now."); exit()


def libimport():
    try:
        import getch
        from pyfiglet import figlet_format as pfg
        import paramiko
        import sqlite3
        return True
    except:
        return False


if not libimport():
    with spinner("Collecting Python libraries..."):
        cmd_run('pip install getch pyfiglet paramiko')
        cmd_run(f'cp -r Host/Host_libs {sys.path[2]}')
        cmd_run(f'cp -r Asterix_libs {sys.path[2]}')
    success('Python libraries collected.')


import getch
import sqlite3
from pyfiglet import figlet_format as pfg


print(pfg('AsterixSETUP'))


if subprocess.run('whoami', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8').strip() != 'root': fail('This program must be run as root.'); exit()


def get_docker():
    with spinner('Installing Docker Engine...'):
        subprocess.call("curl -fsSL https://get.docker.com -o get-docker.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        info('Fetched install script.        ')
        subprocess.call("bash get-docker.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        info('Docker installed.              ')
        subprocess.call("rm get-docker.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call("systemctl start docker", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call("systemctl enable docker", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("docker version", shell=True)
    success('Docker Engine installed.')


if subprocess.run('docker version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stderr.decode('utf-8').strip() == '/bin/sh: 1: docker: not found': warning('Oops, docker is not installed. Installing now !'); get_docker()


if subprocess.Popen('qemu-system-aarch64 -machine help', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() != 0: 
    with spinner('Collecting QEMU KVM...'):
        cmd_run("apt install virt-manager libvirt0 qemu-system -y")
    success('QEMU KVM Installed.')

with spinner('Creating source folders...'):
    if not os.path.exists("/src"): cmd_run("/usr/bin/mkdir /src")
    if len(os.listdir("/src")) != 0: cmd_run("/usr/bin/rm -r /src/*")
    cmd_run('/usr/bin/mkdir /src/win10_VM')
success("Source folders created.")


with spinner('Creating software users'):
    if subprocess.Popen('id docker_runner', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() != 0:
        cmd_run("/usr/sbin/useradd -m -d /opt/docker_runner docker_runner")
    cmd_run("/usr/sbin/usermod -aG docker docker_runner")
    if subprocess.Popen('id vm_runner', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() != 0:
        cmd_run("/usr/sbin/useradd -m -d /opt/vm_runner vm_runner")
        cmd_run("/usr/sbin/usermod -G kvm vm_runner")
    if subprocess.Popen('id asterix', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() != 0:
        cmd_run("/usr/sbin/useradd -m -d /opt/asterix asterix")
success('Software users created.')


with spinner('Preparing Frontend software...'):
    cmd_run("/usr/bin/cp -r Frontend /src/Frontend")
    cmd_run("/usr/bin/cp -r Asterix_libs /src/Frontend")
    cmd_run("/usr/bin/chown -R docker_runner:docker /src/Frontend")
    cmd_run("/usr/bin/chmod -R u=rx /src/Frontend")
    cmd_run("/usr/bin/chmod -R g=rx /src/Frontend")
    cmd_run("/usr/bin/chmod -R o=-r-w-x /src/Frontend")
success("Frontend software ready.")


with spinner('Preparing Backend software...'):
    cmd_run("/usr/bin/cp -r Backend /src/Backend")
    cmd_run("/usr/bin/cp -r Asterix_libs /src/Backend")
    cmd_run("/usr/bin/chown -R docker_runner:docker /src/Backend")
    cmd_run("/usr/bin/chmod -R u=rx /src/Backend")
    cmd_run("/usr/bin/chmod -R g=rx /src/Backend")
    cmd_run("/usr/bin/chmod -R o=-r-w-x /src/Backend")
success("Backend software ready.")


with spinner('Preparing Brain software...'):
    cmd_run("/usr/bin/cp -r Brain /src/Brain")
    cmd_run("/usr/bin/cp -r Asterix_libs /src/Brain")
    cmd_run("/usr/bin/chown -R docker_runner:docker /src/Brain")
    cmd_run("/usr/bin/chmod -R u=rx /src/Brain")
    cmd_run("/usr/bin/chmod -R g=rx /src/Brain")
    cmd_run("/usr/bin/chmod -R o=-r-w-x /src/Brain")
success("Brain software ready.")


with spinner('Collecting PyRATE...'):
    cmd_run("/usr/bin/git clone https://github.com/G4vr0ch3/PyRATE /src/Frontend/PyRATE")
success("Pyrate collected.")


info('Preparing Host software...')
cmd_run('/usr/bin/mkdir -p /src/Host/Administration')
cmd_run('/usr/bin/cp Host/eject_devices.sh /src/Host/eject_devices.sh')
cmd_run('/usr/bin/cp Host/db_create.py /src/Host/db_create.py')
cmd_run('/usr/bin/chmod -R 000 /src/Host')


with spinner('Adding mounting service...'):
    subprocess.run('rm -r /usr/share/Asterix', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cmd_run('mkdir -p /usr/share/Asterix/Mounters')
    cmd_run('/usr/bin/cp Host/Mounters/*.sh /usr/share/Asterix/Mounters/')
    cmd_run('/usr/bin/chmod 777 /usr/share/Asterix/Mounters/*.sh')
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


success('Host software ready.')


with spinner("Building Frontend container. This may take some time..."):
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker build -t frontend /src/Frontend"')
    frontend_img = subprocess.Popen('/usr/bin/docker images --filter=reference=frontend --format "{{.ID}}"', shell = True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
success("Frontend software installed.")


with spinner("Building Backend container. This may take some time..."):
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker build -t backend /src/Backend"')
    backend_img = subprocess.Popen('/usr/bin/docker images --filter=reference=backend --format "{{.ID}}"', shell = True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
success("Backend software installed.")


with spinner("Building Brain container. This may take some time..."):
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker build -t brain /src/Brain"')
    brain_img = subprocess.Popen('/usr/bin/docker images --filter=reference=brain --format "{{.ID}}"', shell = True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
success("Brain software installed.")


with spinner('Creating relevant docker volumes...'): 
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name USBInputDevice"')
    info('USBInputDevice volume created.         ')
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name InputFiles"')
    info('InputFiles volume created.             ')
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name Sanitized"')
    info('Sanitized volume created.              ')
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name USBOutputDevice"')
    info('USBOutputDevice volume created.        ')
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name OutputFiles"')
    info('OutputFiles volume created.            ')
    cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name DataShare"')
    info('DataShare volume created.              ')
success("All relevant docker volumes created.")


with spinner('Starting containers...'):
    cmd_run("/usr/bin/cp Host/docker_runner_scripts/boot.sh /opt/docker_runner/boot.sh")
    cmd_run("/usr/bin/cp Host/docker_runner_scripts/run.sh /opt/docker_runner/run.sh")
    subprocess.run('/usr/bin/su - docker_runner -c "/bin/bash /opt/docker_runner/boot.sh"', shell=True)
    frontend_ctn = subprocess.Popen('/usr/bin/docker ps -aqf "name=frontend"', shell = True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
    backend_ctn = subprocess.Popen('/usr/bin/docker ps -aqf "name=backend"', shell = True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
    brain_ctn = subprocess.Popen('/usr/bin/docker ps -aqf "name=brain"', shell = True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
success("Docker containers started.")


with spinner('Adding component data to Admin DB...'):
    conn=sqlite3.connect('/src/Host/Administration/ASTERIX_ADMIN.db')
    cur= conn.cursor()
    print('Database connection opened.')
    sql= 'SELECT sqlite_version();'
    cur.execute(sql)
    res=cur.fetchall()
    print('SQLite Version : ' + res[0][0])
    cur.execute("""CREATE TABLE IF NOT EXISTS containers (c_name TEXT, c_id TEXT, i_id TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS vms (name TEXT, disk TEXT, hash TEXT)""")
    cur.execute("""INSERT INTO containers(c_name, c_id, i_id) VALUES (?,?,?)""",("frontend",frontend_ctn, frontend_img))
    print(f'Inserted frontend, {frontend_ctn}, {frontend_img}')
    cur.execute("""INSERT INTO containers(c_name, c_id, i_id) VALUES (?,?,?)""",("frontend",backend_ctn, backend_img))
    print(f'Inserted backend, {backend_ctn}, {backend_img}')
    cur.execute("""INSERT INTO containers(c_name, c_id, i_id) VALUES (?,?,?)""",("frontend",brain_ctn, brain_img))
    print(f'Inserted brain, {brain_ctn}, {brain_img}')
    cur.execute("""INSERT INTO vms(name, disk, hash) VALUES (?,?,?)""",("AC-CENTER","/src/win10_VM/system.vhdx", "x5b902ffa10efb18d8066b40cbed89e9a"))
    warning(f'Inserted ACCENTER row with default values.')
    conn.commit()
    cur.close()
    conn.close()
    print('Database connection closed\n')
success('Admin DB set up.')


with spinner('Setting up Administration tools...'):
    cmd_run('/usr/bin/cp Host/Administration/admin_utility.py /src/Host/Administration/admin_utility.py')
success('Administration tools ready.')


with spinner("Fixing user permissions..."):
    cmd_run("/usr/bin/cp Host/Asterix.py /opt/asterix/Asterix.py")
    cmd_run("/usr/bin/chown -R asterix:asterix /opt/asterix")
    cmd_run("/usr/bin/chmod -R 755 /opt/asterix")
    cmd_run("/usr/bin/chown -R docker_runner:docker_runner /opt/docker_runner")
    cmd_run("/usr/bin/chmod -R 755 /opt/docker_runner")
    cmd_run("/usr/bin/chmod -R +r /var/lib/docker/volumes/DataShare/_data")
    cmd_run("chown root:asterix /var/lib/docker")
    cmd_run("chown root:asterix /var/lib/docker/volumes")
    cmd_run("chown root:asterix /var/lib/docker/volumes/DataShare")
    cmd_run("chown root:asterix /var/lib/docker/volumes/DataShare/_data")
    cmd_run("/usr/bin/chmod g=rx /var/lib/docker")
    cmd_run("/usr/bin/chmod g=rx /var/lib/docker/volumes")
    cmd_run("/usr/bin/chmod g=rx /var/lib/docker/volumes/DataShare")
    cmd_run("/usr/bin/chmod g=rx /var/lib/docker/volumes/DataShare/_data")
success('Fixed user permissions.')


info("Seting up AC-Center environment...")


print("Copy VM files to /src/win10_VM and press any key to resume.")
getch.getch()


with spinner('Preparing Windows 10 VM Environment...'):
    cmd_run("/usr/bin/chown -R vm_runner:vm_runner /src/win10_VM")
    cmd_run("/usr/bin/chmod -R u=rx /src/win10_VM")
    cmd_run("/usr/bin/chmod -R g=rx /src/win10_VM")
    cmd_run("/usr/bin/chmod -R o=-r-x-w /src/win10_VM")
success("Win VM source folder created.")


with spinner("Setting up Cron Jobs..."):
    cmd_run("/usr/bin/cp Host/asterix_jobs /etc/cron.d/asterix_jobs")
success("Cron Jobs set up.")


with spinner("Adding sudoers rules..."):
    subprocess.run("/usr/bin/cp Host/010_asterix-nopasswd /etc/sudoers.d/010_asterix-nopasswd", shell = True, stdout=subprocess.PIPE)
subprocess.run("visudo -c", shell = True)
success("Added sudoers rules.")


warning("AC-Center needs to be configured manually, check https://github.com/G4vr0ch3/Asterix/blob/main/AC-Center/README.md")


# SETUP END
success("Exhausted")