#!/bin/bash

# This script is called from our systemd unit file to unmount a USB drive.

MNTBASE="/var/lib/docker/volumes/USBOutputDevice/_data/USBOutputPart/"

# See if this drive is already mounted, and if so where
MOUNTED=$(/bin/mount | /bin/grep ${MNTBASE} | /usr/bin/awk '{ print $3 }')


while [[ ! -z ${MOUNTED} ]]
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

    if [ -z "$(ls -A ${MNTBASE})" ] 
    then
        /bin/rmdir $MNTBASE
    fi

    sleep 1

done