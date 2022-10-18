#!/usr/bin/python3.10

import os
import sqlite3
import paramiko
import subprocess

from time import sleep

from Asterix_libs.spinner import spinner
from Asterix_libs.prints import *
from Asterix_libs.log import *


target = '127.0.0.1'
port = 10022
username = 'ac-center'
password = 'ac-center'

database = 'ASTERIX_ADMIN.db'


def vm_check():

    vms = get_vms()

    if vms == []:
        print('NO VM FOUND IN DATABASE')
        exit()

    else:

        with spinner('Fetching VM Status ...'):

            for vm in vms:
                disk_path = vm[1]
                disk_hash = vm[2]

    with spinner('Computing disk hash...'):
        md5hash = subprocess.Popen(f'/usr/bin/md5sum {disk_path}', shell = True, stdout = subprocess.PIPE).stdout.read().strip().split(" ")[0]
    success(f'Calculated md5 sum : {md5hash}')
    if md5hash != disk_hash:
        warning(f'Hashes do not match {disk_hash}:{md5hash}. VM Might be corrupted.')
        return False
    else:
        success(f'Hashes match {disk_hash}:{md5hash}. VM Checked')
        return True


def cmd_run(cmd):
    if subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() != 0:
        fail('Process failed. This is critical.')
        print(cmd)
        fail("Exiting now.")
        exit()


def test_db():

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        success('Database connection opened.')
        sql = 'SELECT sqlite_version();'
        cur.execute(sql)
        res = cur.fetchall()
        info('SQLite Version : ' + res[0][0])
        return True

    except:
        fail('Database connection failed.')
        return False


def get_containers():

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM containers;""")

    res = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return res


def get_vms():

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM vms;""")

    res = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return res


def get_status_container(container_name, container_id):

    check = subprocess.Popen('/usr/bin/docker ps -aqf "name=' + container_name + '"', shell=True,
                             stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()

    if check != container_id:
        return '\U0001F534 Corrupted'

    stat = subprocess.Popen('/usr/bin/docker inspect -f "{{.State.Status}}" ' + container_id, shell=True,
                            stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()

    if stat == 'exited':
        return '\U0001F7E0 Exited   '
    elif stat == 'running':
        return '\U0001F7E2 Running  '
    else:
        return '\U0001F534 Unknown  '


def get_status_vm(vm_integrity_checked):

    running_vms = subprocess.Popen('ps -ef | grep qemu-system-aarch64', shell=True, stderr=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip().split('\n')[:-2]

    if running_vms == []:
        return '\U0001F7E0 No running VM '

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:

        client.connect(target, port=10022,
                       username=username, password=password)
        transport = client.get_transport()
        if transport.is_active():
            try:
                transport.send_ignore()
                if vm_integrity_checked:
                    return '\U0001F7E2 Connected     '
                else:
                    return '\U0001F535 Connected (UC)'
            except Exception as _e:
                return '\U0001F7E1 Error         '
        else:
            return '\U0001F7E0 Innactive     '

    except:

        return '\U0001F7E0 Innactive     '


def restart_containers():

    containers = get_containers()

    with spinner('Starting containers...'):
        for container in containers:
            subprocess.run(
                f'/usr/bin/su - docker_runner -c "/usr/bin/docker restart {container[1]}"', shell=True, stdout=subprocess.DEVNULL)
            success(f'Container {container[0]} restarted.')

    success('Containers restarted.')


def start_vm():

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    paramiko.util.log_to_file('/dev/null')

    subprocess.run("/bin/bash /src/win10_VM/run.sh &", shell=True)

    with spinner('Restarting VM...'):

        ready = False

        while not ready:

            try:
                client.connect(target, port=10022,
                               username=username, password=password, timeout=1)
                ready = True
            except Exception as _e:
                ready = False

    success('VM restarted.')


def kill_vm():

    running_vms = subprocess.Popen("ps -ef | grep qemu-system-aarch64 | awk '{print $2}'", shell=True,
                                   stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip().split('\n')[:-2]

    with spinner('Killing VMs...'):
        while running_vms != []:

            process = running_vms.pop()

            subprocess.run(f'/usr/bin/kill {process}', shell=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    success('No more running VMs.')


def restart_vm():

    kill_vm()
    start_vm()


def reset_containers():

    containers = get_containers()

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("""DROP TABLE containers;""")

    for container in containers:
        container_name = container[0]
        container_id = container[1]
        container_image = container[2]

        with spinner(f'Killing container {container_name}...'):
            subprocess.call(f'/usr/bin/docker container kill {container_id}',
                            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        info(f'Killed container {container_name}.')

        with spinner(f'Removing container {container_name}...'):
            subprocess.call(f'/usr/bin/docker container rm {container_id} --force',
                            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        info(f'Killed container {container_name}.')

        with spinner(f'Removing container image from {container_name}...'):
            subprocess.call(f'/usr/bin/docker image rm {container_image} --force',
                            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        info(f'Removed container image for {container_name}.')

        with spinner("Building Frontend container. This may take some time..."):
            cmd_run(
                '/usr/bin/su - docker_runner -c "/usr/bin/docker build -t frontend /src/Frontend"')
        success("Frontend software installed.")

        with spinner("Building Backend container. This may take some time..."):
            cmd_run(
                '/usr/bin/su - docker_runner -c "/usr/bin/docker build -t backend /src/Backend"')
        success("Backend software installed.")

        with spinner("Building Brain container. This may take some time..."):
            cmd_run(
                '/usr/bin/su - docker_runner -c "/usr/bin/docker build -t brain /src/Brain"')
        success("Brain software installed.")


def fetch_glob(vm_integrity_checked):

    containers = get_containers()

    if containers == []:
        print(" ________________ ")
        print("| Empty Database |")
        print("|________________|")
        print()
        exit()

    else:
        ct = len(containers)
        container_name_size = (
            min(max([len(container[0]) for container in containers]), 200))
        container_id_size = min(
            max([len(container[1]) for container in containers]), 200)
        print(' ' + "_"*(max(container_name_size, 9) + container_id_size + 25) + ' ')
        print('| Component ' + " "*max(container_name_size - 11, 0) +
              "| ID " + " "*max(container_id_size - 2, 0) + "| Status            |")
        print('|_'+"_"*max(container_name_size, 9) + "_|_" +
              "_"*container_id_size + "_|___________________|")

        with spinner('Fetching Container Status ...'):

            for container in containers:
                container_name = container[0]
                container_id = container[1]
                container_status = get_status_container(
                    container_name, container_id)
                print('| ' + container_name[-container_name_size:] + " "*(max(container_name_size, 11) - len(container_name[-container_name_size:]) - 2) + " | " + container_id[-container_id_size:] + " "*(container_id_size - len(container_id[-container_id_size:])) + " | " + container_status + "      |")

    vms = get_vms()

    if vms == []:
        print('NO VM FOUND IN DATABASE')
        exit()

    else:

        with spinner('Fetching VM Status ...'):

            for vm in vms:
                vm_name = vm[0]
                vm_disk = vm[1]
                vm_hash = vm[2]
                vm_status = get_status_vm(vm_integrity_checked)

                print('| ' + vm_name[-container_name_size:] + " "*(max(container_name_size, 11) - len(
                    vm_name[-container_name_size:]) - 2) + " | " + vm_hash[-container_id_size:] + " "*(container_id_size - len(vm_hash[-container_id_size:])) + " | " + vm_status + " |")

    print('|_'+"_"*max(container_name_size, 9) + "_|_" +
          "_"*container_id_size + "_|___________________|")


def usb_enroll():
    with spinner("Plug USB drive to enroll in Input port..."):
    
        while not os.path.exists("/dev/USBInputDisk"):
            sleep(.5)

    idProduct=os.popen(f'udevadm info -q all -a /dev/USBInputDisk | grep idProduct | cut -d "=" -f 3 | head -n 1').read().strip()
    idVendor=os.popen(f'udevadm info -q all -a /dev/USBInputDisk | grep idVendor | cut -d "=" -f 3 | head -n 1').read().strip()
    conn=sqlite3.connect('/src/Host/Administration/USB_ID.db')
    cur= conn.cursor()
    print('Database connection opened.')
    sql= 'SELECT sqlite_version();'
    cur.execute(sql)
    res=cur.fetchall()
    print('SQLite Version : ' + res[0][0])
    print("Known drives table checked.")
    cur.execute("""INSERT INTO known_drives(idVendor,idProduct) VALUES (?,?)""",(idVendor,idProduct))
    print(f'Inserted ({idVendor},{idProduct})')
    conn.commit()
    cur.close()
    conn.close()
    print('Database connection closed\n')

    cmd_run('/bin/cp /src/Host/Administration/USB_ID.db /var/lib/docker/volumes/DataShare/_data/USB_ID.db')


def main():

    vm_integrity_checked = False

    while True:

        try:

            fetch_glob(vm_integrity_checked)

            print("""
Actions :

1) Restart all
2) Restart Containers
3) RESET CONTAINERS
4) Restart VMs
5) VMs check
6) VM RESET
7) Log check
8) Enroll new trusted USB device
q) Exit

""")
            try:
                choice = str(input('>>> '))[0]
            except:
                fail('Invalid choice.')
                exit()

            if choice == "q":
                success('Bye !')
                exit()

            elif choice == "1":
                info('Selected Full restart.')
                restart_containers()
                restart_vm()

            elif choice == "2":
                info('Selected Container restart.')
                restart_containers()

            elif choice == "3":
                info('Selected Container RESET.')
                reset_containers()

            elif choice == "4":
                info('Selected VM restart.')
                restart_vm()

            elif choice == "5":
                vm_integrity_checked = vm_check()

            elif choice == "6":
                info('Selected VM RESET.')
                reset_vm()

            elif choice == "7":
                info('Selected log check.')
                log_check()

            elif choice == "8":
                info('Selected new USB device enrolment.')
                usb_enroll()

        except KeyboardInterrupt:

            exit()


if __name__ == "__main__":

    try:
        if not test_db():
            exit()
        main()

    except KeyboardInterrupt:
        fail("KEYBOARD INTERRUPT")
        exit()
