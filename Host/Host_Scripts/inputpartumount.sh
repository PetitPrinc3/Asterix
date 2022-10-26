#!/bin/bash

# This script is called from our systemd unit file to unmount a USB drive.

MNTBASE="/var/lib/docker/volumes/USBInputDevice/_data/USBInputPart/"

# See if this drive is already mounted, and if so where
MOUNTED=$(/bin/mount | /bin/grep ${MNTBASE} | /usr/bin/awk '{ print $3 }')


while [[ -d $MNTPOINT ]]
do
    if [[ -z ${MOUNTED} ]]
    then
        echo "Warning: Device is not mounted"
    else
        for dev in `ls $MNTBASE`
        do
            /bin/umount $MNTBASE$dev
        echo "**** Unmounted ${dev}"
    fi

    if ! /bin/rmdir $MNTPOINT
    then
        echo "Failed to remove mountpoint"
    fi

    if [ -z "$(ls -A ${MNTBASE})" ] 
    then
        /bin/rmdir $MNTBASE
    fi

    sleep 1

done