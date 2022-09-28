#!/bin/bash
qemu-system-aarch64 -cpu host -M virt,accel=kvm -smp 3 -m 4096 -drive file=/src/win10_VM/AAVMF_CODE.fd,format=raw,if=pflash,index=0,readonly=on -drive file=/src/win10_VM/AAVMF_VARS.fd,format=raw,if=pflash,index=1 -device ramfb -device nec-usb-xhci -device usb-kbd -device usb-mouse -device usb-tablet -device nvme,drive=systemDisk,serial=systemDisk -drive if=none,id=systemDisk,format=raw,file=/src/win10_VM/system.vhdx -device usb-storage,drive=drivers,serial=drivers -drive if=none,id=drivers,format=raw,media=cdrom,file=/src/win10_VM/virtio_drivers.iso -device usb-storage,drive=install,serial=install -drive if=none,id=install,format=raw,media=cdrom,file=/src/win10_VM/winarm.iso