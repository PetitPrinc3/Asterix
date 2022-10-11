#!/bin/bash

/usr/bin/systemctl stop inppartmnt@$(udevadm info -q all -a /dev/USBInputPart | grep KERNEL | head -n 1 | cut -d '"' -f 2).service
/usr/bin/systemctl stop inpdiskmnt@$(udevadm info -q all -a /dev/USBInputDisk | grep KERNEL | head -n 1 | cut -d '"' -f 2).service

/usr/bin/systemctl stop outpartmnt@$(udevadm info -q all -a /dev/USBOutputPart | grep KERNEL | head -n 1 | cut -d '"' -f 2).service
/usr/bin/systemctl stop outdiskmnt@$(udevadm info -q all -a /dev/USBOutputDisk | grep KERNEL | head -n 1 | cut -d '"' -f 2).service