#!/bin/bash

/usr/bin/systemctl stop inputpartmnt@$(udevadm info -q all -a /dev/USBInputPart | grep KERNEL | head -n 1 | cut -d '"' -f 2).service

/usr/bin/systemctl stop outppartmnt@$(udevadm info -q all -a /dev/USBOutputPart | grep KERNEL | head -n 1 | cut -d '"' -f 2).service