#!/bin/bash

for i in `ls /dev/USBInputPart*`
do
    /usr/bin/systemctl stop inputpartmnt@$(udevadm info -q all -a $i | grep KERNEL | head -n 1 | cut -d '"' -f 2).service
done

for i in `ls /dev/USBOutputPart*`
do
    /usr/bin/systemctl stop outppartmnt@$(udevadm info -q all -a $i | grep KERNEL | head -n 1 | cut -d '"' -f 2).service
done