import subprocess

from Asterix_libs.prints import *

from Host_libs import usb_detection as ud


def Frontend():

    inp = ud.inp_wait(["/dev/USBInputPart", "/dev/USBInputDisk", "/dev/USBBadInput"])
    if inp is None : fail('Input detection failed.'); exit()

    if inp == "/dev/USBBadInput": warning('The USB Input drive was detected as a BAD INPUT. Please contact your admnistrator.'); fail('Process terminated. This incident will be reported'); exit()

    subprocess.run(f'sudo /usr/bin/mount {inp} /var/lib/docker/volumes/USBInputDevice/_data', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run(f'su - docker_runner -c "/usr/bin/docker exec -w /usr/share/USBHandler -it frontend python3 main.py"', shell=True)

    subprocess.run(f'sudo /usr/bin/umount {inp}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def Backend():

    outp = ud.inp_wait(["/dev/USBOutputPart", "/dev/USBOutputDisk"])
    if outp is None: fail('Output detection failed.'); exit()

    subprocess.run(f'sudo /usr/bin/mount {outp} /mnt/USBOutputDevice', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    success('Done. Thank you for using Asterix <3')


if __name__ == '__main__':
    Frontend()