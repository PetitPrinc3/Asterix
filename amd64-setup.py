#!/usr/bin/python3

import subprocess
import sqlite3
import sys
import os


from re import sub
from time import sleep


if subprocess.run('whoami', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8').strip() != 'root':
    fail('This program must be run as root.')
    exit()


def cmd_run(cmd):
    try:
        if subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait(timeout=600) != 0:
            warning('Process failed once. Trying again.')
            try:
                if subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait(timeout=600) != 0:
                    fail('Process failed. This is critical.                                                  ')
                    print(cmd)
                    fail("Exiting now.")
                    exit(1)
            except subprocess.TimeoutExpired:
                    fail('Command timed out. This is critical.                                               ')
                    print(cmd)
                    fail("Exiting now.")
                    exit(1)

    except subprocess.TimeoutExpired:
        warning('Command timed out. Trying again.')
        try:
            if subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait(timeout=600) != 0:
                fail('Process failed. This is critical.')
                print(cmd)
                fail("Exiting now.")
                exit(1)
        except subprocess.TimeoutExpired:
                fail('Command timed out. This is critical.')
                print(cmd)
                fail("Exiting now.")
                exit(1)


cmd_run(f'cp -r Host/Host_libs {sys.path[2]}')
cmd_run(f'cp -r Asterix_libs {sys.path[2]}')

from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner


try:
    import getch
    from pyfiglet import figlet_format as pfg
    import paramiko
    import sqlite3
except:
    with spinner("Collecting Python libraries..."):
        cmd_run('pip install getch pyfiglet paramiko')
        import getch
        from pyfiglet import figlet_format as pfg
    success('Python libraries collected.')

try:
    print(pfg('AsterixSETUP'))


    def get_docker():
        with spinner('Installing Docker Engine...'):
            cmd_run("curl -fsSL https://get.docker.com -o get-docker.sh")
            info('Fetched install script.        ')
            cmd_run("/bin/bash get-docker.sh")
            info('Docker installed.              ')
            cmd_run("rm get-docker.sh")
            cmd_run("systemctl start docker")
            cmd_run("systemctl enable docker")
        subprocess.call("docker version", shell=True)
        success('Docker Engine installed.')


    if subprocess.run('docker version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stderr.decode('utf-8').strip() == '/bin/sh: 1: docker: not found':
        warning('Oops, docker is not installed. Installing now !')
        get_docker()


    if subprocess.Popen('qemu-system-aarch64 -machine help', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() != 0:
        with spinner('Collecting QEMU KVM...'):
            cmd_run("apt install virt-manager libvirt0 qemu-system -y")
        success('QEMU KVM Installed.')

    with spinner('Creating source folders...'):
        if not os.path.exists("/src"):
            cmd_run("/usr/bin/mkdir /src")
        if len(os.listdir("/src")) != 0:
            cmd_run("/usr/bin/rm -r /src/*")
        cmd_run('/usr/bin/mkdir /src/win10_VM')
    success("Source folders created.")


    with spinner('Converting software for AMD64...'):
        cmd_run('/usr/bin/mv Host/Services/accenter_start.service Host/Services/accenter_start.service.old')
        with open("Host/Services/accenter_start.service", "w") as nserv:
            serv = """
[Unit]
Description=Start AC-Center on boot

[Service]
Type=simple
User=vm_runner
Group=vm_runner
RemainAfterExit=true
ExecStart=/usr/bin/virsh --connect qemu:///system start win10
ExecStop=/usr/bin/virsh shutdown win10

[Install]
WantedBy=multi-user.target

"""
            nserv.write(serv)

        cmd_run("""running_vms = subprocess.Popen("virsh list | grep win10", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split("\\n")""")

        cmd_run('/usr/bin/mv Host/UDEV/00-backend.rules Host/UDEV/00-backend.rules.old')

        with open("Host/UDEV/00-backend.rules", "w") as nrule:

            n = """
ACTION=="add", KERNEL=="sd[a-z][0-9]", ATTRS{devpath}=="2.2", ENV{DEVTYPE}=="partition", SYMLINK+="USBOutputPart%k", RUN+="/usr/bin/systemctl restart outputpartmnt@%k.service"
ACTION=="add", ATTRS{devpath}=="2.2", KERNEL=="hid*", RUN+="/bin/bash -c '/usr/bin/echo 0 > /var/lib/docker/volumes/DataShare/_data/BadUSBOutput'", RUN+="/bin/bash -c '/usr/bin/echo 0 > /sys/bus/usb/devices/1-2.2/authorized'"
ACTION=="add", ATTRS{devpath}=="2.2", KERNEL=="net*", RUN+="/bin/bash -c '/usr/bin/echo 0 > /var/lib/docker/volumes/DataShare/_data/BadUSBInput'", RUN+="/bin/bash -c '/usr/bin/echo 0 > /sys/bus/usb/devices/1-2.2/authorized'"

ACTION=="remove", ATTRS{devpath}=="2.2", RUN+="/usr/bin/systemctl stop outputpartmnt@*.service"
"""

            nrule.write(n)

        cmd_run('/usr/bin/mv Host/UDEV/00-frontend.rules Host/UDEV/00-frontend.rules.old')

        with open("Host/UDEV/00-frontend.rules", "w") as nrule:

            nrule.write("""
ACTION=="add", KERNEL=="sd[a-z][0-9]", ATTRS{devpath}=="2.1", ENV{DEVTYPE}=="partition", SYMLINK+="USBInputPart%k", RUN+="/usr/bin/systemctl start inputpartmnt@%k.service"
ACTION=="add", ATTRS{devpath}=="2.1", KERNEL=="hid*", RUN+="/bin/bash -c '/usr/bin/echo 0 > /var/lib/docker/volumes/DataShare/_data/BadUSBInput'", RUN+="/bin/bash -c '/usr/bin/echo 0 > /sys/bus/usb/devices/1-2.1/authorized'"
ACTION=="add", ATTRS{devpath}=="2.1", KERNEL=="net*", RUN+="/bin/bash -c '/usr/bin/echo 0 > /var/lib/docker/volumes/DataShare/_data/BadUSBInput'", RUN+="/bin/bash -c '/usr/bin/echo 0 > /sys/bus/usb/devices/1-2.1/authorized'"

ACTION=="remove", ATTRS{devpath}=="2.1", RUN+="/usr/bin/systemctl stop inputpartmnt@*.service"
""")

        rp_lines = open("Brain/PythonHandler/PywavaAutomation/runs_pywava.py", "r").readlines()

        with open("Brain/PythonHandler/PywavaAutomation/runs_pywava.py", "w") as rp:

            for line in rp_lines:

                if "channel.exec_command" in line:
                    l = line.split(" -f")
                    line = f'{l[0]}k -f{l[1]}'

                rp.write(line)

    success("Software converted to AMD64")


    with spinner('Creating software users'):
        if subprocess.Popen('id docker_runner', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() != 0:
            cmd_run("/usr/sbin/useradd -m -d /opt/docker_runner docker_runner")
        cmd_run("/usr/sbin/usermod -aG docker docker_runner")
        if subprocess.Popen('id vm_runner', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() != 0:
            cmd_run("/usr/sbin/useradd -m -d /opt/vm_runner vm_runner")
            cmd_run("/usr/sbin/usermod -G libvirt vm_runner")
        if subprocess.Popen('id asterix', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() != 0:
            cmd_run("/usr/sbin/useradd -m -d /opt/asterix asterix")
        if subprocess.Popen('id asterix_admin', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() != 0:
            cmd_run("/usr/sbin/useradd asterix_admin")
    success('Software users created.')


    info('Setup new asterix_admin password :')
    subprocess.call('passwd asterix_admin', shell=True)
    success('Done.')


    info('Setup new root password :')
    subprocess.call('passwd root', shell=True)
    success('Done.')


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
    cmd_run('/usr/bin/mkdir -p /src/Host/Host_Scripts')
    cmd_run('/usr/bin/cp Host/Host_Scripts/eject_devices.sh /src/Host/Host_Scripts/eject_devices.sh')
    cmd_run('/usr/bin/cp Host/Administration/db_create.py /src/Host/Administration/db_create.py')
    cmd_run('/usr/bin/chmod -R 000 /src/Host')


    with spinner('Adding mounting scripts...'):
        subprocess.run('rm -r /usr/share/Asterix', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cmd_run('mkdir -p /usr/share/Asterix/Mounters')
        cmd_run('/usr/bin/cp Host/Host_Scripts/inputpartmnt.sh /usr/share/Asterix/Mounters/')
        cmd_run('/usr/bin/cp Host/Host_Scripts/inputpartumnt.sh /usr/share/Asterix/Mounters/')
        cmd_run('/usr/bin/cp Host/Host_Scripts/outputpartmnt.sh /usr/share/Asterix/Mounters/')
        cmd_run('/usr/bin/cp Host/Host_Scripts/outputpartumnt.sh /usr/share/Asterix/Mounters/')
        cmd_run('/usr/bin/chmod =rx /usr/share/Asterix/Mounters/*.sh')
    success('Created mounting service.')


    with spinner('Adding UDEV rules...'):
        cmd_run("/usr/bin/cp Host/UDEV/00-frontend.rules /etc/udev/rules.d")
        cmd_run("/usr/bin/cp Host/UDEV/00-backend.rules /etc/udev/rules.d")
        info('Reloading rules...      ')
        cmd_run("udevadm control --reload-rules")
        info('Triggering rules...     ')
        cmd_run("udevadm trigger")
    success("UDEV rules added.")


    with spinner('Creating Systemd services...'):
        cmd_run('/usr/bin/cp Host/Services/frontend_start.service /etc/systemd/system/')
        cmd_run('/usr/bin/cp Host/Services/backend_start.service /etc/systemd/system/')
        cmd_run('/usr/bin/cp Host/Services/brain_start.service /etc/systemd/system/')
        cmd_run('/usr/bin/cp Host/Services/accenter_start.service /etc/systemd/system/')
        cmd_run('/usr/bin/cp Host/Services/inputpartmnt@.service /etc/systemd/system/')
        cmd_run('/usr/bin/cp Host/Services/outputpartmnt@.service /etc/systemd/system/')
        cmd_run('/usr/bin/cp Host/Services/temporary_perm_fix.service /etc/systemd/system/')
        cmd_run('systemctl daemon-reload')
        cmd_run('systemctl enable accenter_start.service')
        cmd_run('systemctl enable frontend_start.service')
        cmd_run('systemctl enable backend_start.service')
        cmd_run('systemctl enable brain_start.service')
        cmd_run('systemctl enable temporary_perm_fix.service')
    success('Created systemd service.')


    with spinner("Adding sudoers rules..."):
        subprocess.run("/usr/bin/cp Host/Sudoers/010_asterix-nopasswd /etc/sudoers.d/010_asterix-nopasswd", shell=True, stdout=subprocess.PIPE)
        subprocess.run("/usr/bin/cp Host/Sudoers/010_asterix_admin /etc/sudoers.d/010_asterix_admin", shell=True, stdout=subprocess.PIPE)
        cmd_run('/usr/bin/chmod 0440 /etc/sudoers.d/010_asterix-nopasswd')
        cmd_run('/usr/bin/chmod 0440 /etc/sudoers.d/010_asterix_admin')
    subprocess.run("visudo -c", shell=True)
    success("Added sudoers rules.")


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


    with spinner("Fixing user permissions..."):

        cmd_run('/usr/bin/cp Host/Asterix.py /opt/asterix/Asterix.py')
        cmd_run('/usr/bin/chown -R asterix:asterix /opt/asterix')
        cmd_run('/usr/bin/chmod -R u=rwx /opt/asterix')
        cmd_run('/usr/bin/chmod -R g=rwx /opt/asterix')
        cmd_run('/usr/bin/chmod -R o=-r-w-x /opt/asterix')
        cmd_run('/usr/bin/chown -R docker_runner:docker_runner /opt/docker_runner')
        cmd_run('/usr/bin/chmod -R u=rwx /opt/docker_runner')
        cmd_run('/usr/bin/chmod -R g=rwx /opt/docker_runner')
        cmd_run('/usr/bin/chmod -R o=-r-w-x /opt/docker_runner')
        cmd_run('systemctl start temporary_perm_fix.service')

    success('Fixed user permissions.')


    with spinner('Created known USB drives Database...'):
        subprocess.run('/usr/bin/python /src/Host/Administration/db_create.py', shell=True, stderr=subprocess.DEVNULL)
    success('Done setting up known USB database.')


    with spinner('Setting up Administration tools...'):
        cmd_run('/usr/bin/cp Host/Administration/admin_utility.py /src/Host/Administration/admin_utility.py')
        cmd_run('/usr/bin/cp Host/Administration/asterix-admin /bin/asterix-admin')
        cmd_run('/usr/bin/chmod u=rx /bin/asterix-admin')
        cmd_run('/usr/bin/chmod g=rx /bin/asterix-admin')
        cmd_run('/usr/bin/chmod o=-r-w-x /bin/asterix-admin')
    success('Administration tools ready.')


    success('Host software ready.')


    with spinner("Building Frontend container. This may take some time..."):
        cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker build -t frontend /src/Frontend"')
        frontend_img = subprocess.Popen('/usr/bin/docker images --filter=reference=frontend --format "{{.ID}}"', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
    success("Frontend software installed.")


    with spinner("Building Backend container. This may take some time..."):
        cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker build -t backend /src/Backend"')
        backend_img = subprocess.Popen('/usr/bin/docker images --filter=reference=backend --format "{{.ID}}"', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
    success("Backend software installed.")


    with spinner("Building Brain container. This may take some time..."):
        cmd_run('/usr/bin/su - docker_runner -c "/usr/bin/docker build -t brain /src/Brain"')
        brain_img = subprocess.Popen('/usr/bin/docker images --filter=reference=brain --format "{{.ID}}"', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
    success("Brain software installed.")


    with spinner('Starting containers...'):
        cmd_run("/usr/bin/cp Host/docker_runner_scripts/boot.sh /opt/docker_runner/boot.sh")
        subprocess.run('/usr/bin/su - docker_runner -c "/bin/bash /opt/docker_runner/boot.sh"', shell=True)
        frontend_ctn = subprocess.Popen('/usr/bin/docker ps -aqf "name=frontend"', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
        backend_ctn = subprocess.Popen('/usr/bin/docker ps -aqf "name=backend"', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
        brain_ctn = subprocess.Popen('/usr/bin/docker ps -aqf "name=brain"', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
    success("Docker containers started.")


    info("Seting up AC-Center environment...")


    print("Copy VM files to /src/win10_VM and press any key to resume.")
    getch.getch()


    with spinner('Preparing Windows 10 VM Environment...'):
        cmd_run("/usr/bin/cp AC-Center/vm_run.sh /src/win10_VM/vm_run.sh")
        cmd_run("/usr/bin/chown -R vm_runner:vm_runner /src/win10_VM")
        cmd_run("/usr/bin/chmod -R u=rwx /src/win10_VM")
        cmd_run("/usr/bin/chmod -R g=rwx /src/win10_VM")
        cmd_run("/usr/bin/chmod -R o=-r-x-w /src/win10_VM")
    success("Win VM source folder created.")


    warning("AC-Center needs to be configured manually, check https://github.com/G4vr0ch3/Asterix/blob/main/AC-Center/README.md")


    print('Do you wish to start the AC-Center using default values ? (Y/n)')
    try:
        choice = str(input('>>> '))[0].lower()

        if choice == 'n':
            success('Skip starting AC-Center.')

        elif choice == 'y':
            success('Starting AC Center.')

            import paramiko

            target = '127.0.0.1'
            port = 10022
            username = 'ac-center'
            password = 'ac-center'

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            paramiko.util.log_to_file('/dev/null')

            subprocess.run("/usr/bin/systemctl restart accenter_start", shell=True)

            with spinner('Restarting VM...'):

                ready = False
                tmout = 0

                while not ready and tmout < 120:

                    try:
                        client.connect(target, port=10022,
                                    username=username, password=password, timeout=1)
                        ready = True

                    except KeyboardInterrupt:
                        success('Skipped')
                        break

                    except Exception as _e:
                        ready = False
                        tmout += 1
                        sleep(1)

            if ready and tmout < 120: success('VM restarted.')
            elif ready and tmout >= 120: fail('VM timed out.')
            else: warning('VM not ready.')

    except KeyboardInterrupt:
        success('Skipped.')


    with spinner('Adding component data to Admin DB...'):
        conn = sqlite3.connect('/src/Host/Administration/ASTERIX_ADMIN.db')
        cur = conn.cursor()
        info('Database connection opened.             ')
        sql = 'SELECT sqlite_version();'
        cur.execute(sql)
        res = cur.fetchall()
        info('SQLite Version : ' + res[0][0] + '      ')
        cur.execute("""CREATE TABLE IF NOT EXISTS containers (c_name TEXT, c_id TEXT, i_id TEXT)""")
        info('Created containers table')
        cur.execute("""CREATE TABLE IF NOT EXISTS vms (name TEXT, disk TEXT, hash TEXT)""")
        info('Created vms table')
        cur.execute("""INSERT INTO containers(c_name, c_id, i_id) VALUES (?,?,?)""", ("frontend", frontend_ctn, frontend_img))
        info(f'Inserted frontend, {frontend_ctn}, {frontend_img}')
        cur.execute("""INSERT INTO containers(c_name, c_id, i_id) VALUES (?,?,?)""", ("backend", backend_ctn, backend_img))
        info(f'Inserted backend, {backend_ctn}, {backend_img}')
        cur.execute("""INSERT INTO containers(c_name, c_id, i_id) VALUES (?,?,?)""", ("brain", brain_ctn, brain_img))
        info(f'Inserted brain, {brain_ctn}, {brain_img}        ')
        cur.execute("""INSERT INTO vms(name, disk, hash) VALUES (?,?,?)""", ("ACCENTER", "/src/win10_VM/system.vhdx", "5b902ffa10efb18d8066b40cbed89e9a"))
        warning(f'Inserted ACCENTER row with default values.')
        cur.execute("""CREATE TABLE IF NOT EXISTS logs (date TEXT, path TEXT, content TEXT)""")
        info('Created logs table')
        conn.commit()
        cur.close()
        conn.close()
        info('Database connection closed              ')
    success('Admin DB set up.')


    with spinner("Backing up VM disk..."):

        try:
            if os.path.exists("/src/win10_VM/system.vhdx"):
                cmd_run('/usr/bin/mkdir -p /src/win10_VM/Backup')
                cmd_run('/usr/bin/chown -R asterix_admin:asterix_admin /src/win10_VM/Backup')
                cmd_run('/usr/bin/chmod -R u=rx /src/win10_VM/Backup')
                cmd_run('/usr/bin/chmod -R g=rx /src/win10_VM/Backup')
                cmd_run('/usr/bin/chmod -R o=-r-w-x /src/win10_VM/Backup')
                cmd_run('/usr/bin/cp /src/win10_VM/system.vhdx /src/win10_VM/Backup/System_Backup.vhdx')
                success('VM Disk backed up.')

            else:
                fail('No DISK found to backup.')
                
        except KeyboardInterrupt:
            warning('Backup skipped.')


    cmd_run('/usr/bin/cp Host/Host_Scripts/setup_finish.sh /src/Host/Host_Scripts')


    warning('A reboot is required to complete the setup.')


    # SETUP END
    success("Exhausted")

except Exception as e:
    fail("Somtehing bad happened.")
    print("""

\   /          \   / 
 \ /            \ /  
 / \            / \  
/   \          /   \ 
                     
  ________________   
/                  \ 

""")

    print(e)
    exit()
