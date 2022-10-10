# Asterix : The Analysis Center

![Asterix](../Images/banner.png)

#

The Analysys Center is one of the 4 components that make Asterix.  
Its purpose is to handle the anti-viruses solutions and conduct file analysis.

It is a Windows powered virtual machine.

To better understand the role of the Analysis Center, refer to [this](../README.md#the-project-under-construction) section.

# Installation Instructions

## AC-Center for ARM devices

### Windows 10 ARM Virtual Machine (QEMU - Raspberry Pi 4B)

> :information_source: The VM was created under /src/win10_VM

### :round_pushpin: Download Windows

> Refer : [https://uupdump.net](https://uupdump.net)

Legally download a Windows 10 OS copy and ISO converter from UUPDUMP. Extarct the files from the ZIP file and run the relevant script, accordingly with your OS.

To do this automatically on Linux, you can run the following script : [win_down.py](win_down.py)

```bash

#!/bin/bash

UUID=$(/usr/bin/wget --no-check-certificate -qO- "https://uupdump.net/known.php?q=windows+10+21h2+arm64" | grep 'href="\./selectlang\.php?id=.*"' -o | sed 's/^.*id=//g' | sed 's/"$//g' | head -n1)
WIN_LANG="en-us"

/usr/bin/mkdir -p /src/win10_VM/tmp

/usr/bin/wget --no-check-certificate -O "/src/win10_VM/tmp/uupdump.zip" "https://uupdump.net/get.php?id={UUID}&pack={WIN_LANG}&edition=professional&autodl=2"

cd /src/win10_VM/tmp

/usr/bin/unzip -q "uupdump.zip"
/bin/bash uup_download_linux.sh

mv *.ISO ../winarm.iso

```

### :round_pushpin: Get VirtIO drivers from Fedora

> Refer : [https://fedorapeople.org/groups/virt/virtio-win](https://fedorapeople.org/groups/virt/virtio-win)

Download a copy of Fedora VirtIO Drivers from the Fedora People website.

In our use-case, we used the following :

```bash

/usr/bin/wget --no-check-certificate -O /src/win10_VM/virtio_drivers.iso https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/virtio-win-0.1.221-1/virtio-win-0.1.221.iso

```


### :round_pushpin: Copy the UEFI Firmware

Copy the UEFI Firmware from your linux installation :
- /usr/share/AAVMF/AAVMF_CODE.fd
- /usr/share/AAVMF/AAVMF_VARS.fd

Or do it from the command line with :

```bash

/usr/bin/cp /usr/share/AAVMF/AAVMF_CODE.fd /src/win10_VM/AAVMF_CODE.fd 
/usr/bin/cp /usr/share/AAVMF/AAVMF_VARS.fd /src/win10_VM/AAVMF_VARS.fd

```

### :round_pushpin: Create Filesystem VHX disk

Create a filesystem virtual disk for the VM using qemu-img (We decided to use a 64Gb disk) :

```bash
/usr/bin/qemu-img create -f vhdx -o subformat=fixed /src/win10_VM/system.vhdx 64G
```

### :round_pushpin: Setup Windows

Run [vm_setup.sh](vm_setup.sh) to run the VM and install windows as you would for a regular VM.

```
qemu-system-aarch64 -cpu host -M virt,accel=kvm -smp 3 -m 4096 \
    -drive file=/src/win10_VM/AAVMF_CODE.fd,format=raw,if=pflash,index=0,readonly=on -drive file=/src/win10_VM/AAVMF_VARS.fd,format=raw,if=pflash,index=1 \
    -device ramfb -device nec-usb-xhci -device usb-kbd -device usb-mouse -device usb-tablet \
    -device nvme,drive=systemDisk,serial=systemDisk -drive if=none,id=systemDisk,format=raw,file=/src/win10_VM/system.vhdx \
    -device usb-storage,drive=drivers,serial=drivers -drive if=none,id=drivers,format=raw,media=cdrom,file=/src/win10_VM/virtio_drivers.iso \
    -device usb-storage,drive=install,serial=install -drive if=none,id=install,format=raw,media=cdrom,file=/src/win10_VM/winarm.iso
```

For our use case, we created a "ac-center" user.


### Configuring the environment

### :round_pushpin: Start the VM

To run the VM, use [vm_run.sh](vm_run.sh).

```bash
qemu-system-aarch64 -cpu host -M virt,accel=kvm -smp 3 -m 4096 \
-drive file=/src/win10_VM/AAVMF_CODE.fd,format=raw,if=pflash,index=0,readonly=on -drive file=/src/win10_VM/AAVMF_VARS.fd,format=raw,if=pflash,index=1 \
-device ramfb -device nec-usb-xhci -device usb-kbd -device usb-mouse -device usb-tablet \
-device nvme,drive=systemDisk,serial=systemDisk -drive if=none,id=systemDisk,format=raw,file=/src/win10_VM/system.vhdx \
-device usb-storage,drive=drivers,serial=drivers -drive if=none,id=drivers,format=raw,media=cdrom,file=/src/win10_VM/virtio_drivers.iso \
-net user,hostfwd=tcp::10022-:22 -net nic
```

(After the setup, add the "-display none" flag to the previous script to run the VM in the background.)


### :round_pushpin: Install SSH

> Refer : [Microsoft - Install OpenSSH](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=gui)

Instal OpenSSH server and OpenSSH client as you would on a regular windows machine :

>Both OpenSSH components can be installed using Windows Settings on Windows Server 2019 and Windows 10 devices.
>
>To install the OpenSSH components:
>
>Open Settings, select Apps, then select Optional Features.
>
>Scan the list to see if the OpenSSH is already installed. If not, at the top of the page, select Add a feature, then:
>
>- Find OpenSSH Client, then select Install
>- Find OpenSSH Server, then select Install
>
>Once setup completes, return to Apps and Optional Features and you should see OpenSSH listed.

It is possible that this setup fails, no worries, continue with the instructions.  

Copy ```C:\Windows\System32\OpenSSH``` to ```C:\Windows\SysWOW64``` and open a PowerShell window here.  
Execute ```ssh-keygen``` and follow the instructions (you can keep the default values).  
Execute ```Install-Module -Name OpenSSHUtils -RequiredVersion 0.0.2.0```.

Download OpenSSH-Win64.zip from the [0.0.15.0 Release of OpenSSH](https://github.com/PowerShell/Win32-OpenSSH/releases/tag/v0.0.15.0) and extract its content.   
Copy the extracted files to ```C:\Windows\SysWOW64\OpenSSH``` without overwriting any existing files (skip).
Back to the PowerShell window, execute ```.\FixHostFilePermissions```. You may need to change PowerShell's execution policy using ```Set-ExecutionPolicy Bypass```. (Read about the security involvements of the latter)

You can now start the OpenSSH Server service from Window's Service manager and automatically start it at reboot.

### :round_pushpin: Install Python

> Refer : [Python](https://www.python.org/)

Get a copy from Python ARM64 Installer for Windows on [Python's website](https://www.python.org/downloads/windows/) and install it as you would on a regular machine. Make sure you add Python to the System's path.


### :round_pushpin: Install ClamAV

> Refer : [ClamAV Documentation](https://docs.clamav.net/)

Get a copy from the last Win-32bit msi installer on [ClamAV's Website](https://www.clamav.net/downloads) and follow the instructions given in the documentation to install and configure ClamAV.


### :round_pushpin: Install PyWAVA

> Refer : [PyWAVA](https://github.com/G4vr0ch3/PyWAVA)

Download PyWAVA from Github :
```bash
git clone https://github.com/G4vr0ch3/PyWAVA
```

> :bangbang: PyWAVA's location on the machine needs to be specified to ASTERIX. For every release, you can find PyWAVA's installation location in the release notes. If you decide to install it somewhere else, you will need to edit ASTERIX's source accordingly.

Then in a CMD Prompt in PyWAVA's folder, run ```python setup.py```.

### Conclusion

You're done, you've successfully setup the virtualized environment for the AC-Center.