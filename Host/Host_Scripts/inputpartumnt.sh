#!/bin/bash

# This script is called from our systemd unit file to unmount a USB drive.

MNTBASE="/var/lib/docker/volumes/USBInputDevice/_data/USBInputPart/"

# See if this drive is already mounted, and if so where
MOUNTED=$(/bin/mount | /bin/grep ${MNTBASE} | /usr/bin/awk '{ print $3 }')


while [[ ! -z $MOUNTED ]]
do
    for dev in `ls $MNTBASE`
    do
        /bin/umount /dev/$dev
        echo "**** Unmounted ${dev}"
        
        if ! /bin/rmdir $MNTBASE$dev
        then
            echo "Failed to remove mountpoint"
        fi

    done

    sleep 1

done

if [ -z $(ls ${MNTBASE}) ] 
then
    /bin/rmdir $MNTBASE
fi
