#!/bin/bash

# This script is called from our systemd unit file to mount or unmount a USB drive.

usage()
{
    echo "Usage: $0 {add|remove} device_name (e.g. sdb1) mount_point (e.g. /mnt/USBDrive)"
    exit 1
}

if [[ $# -gt 2 ]]; then
    usage
fi

ACTION=$1
DEVBASE=$2
DEVICE="/dev/${DEVBASE}"
MNTBASE="/var/lib/docker/volumes/USBOutputDevice/_data/USBOutputPart/"
MNTPOINT=$MNTBASE$DEVBASE

# See if this drive is already mounted, and if so where
MOUNTED=$(/bin/mount | /bin/grep ${DEVICE} | /usr/bin/awk '{ print $3 }')

do_mount()
{
    if [[ -n ${MOUNTED} ]]
    then
        echo "Warning: ${DEVICE} is already mounted at ${MOUNTED}"
        exit 1
    fi

    # Get info for this drive: $ID_FS_LABEL, $ID_FS_UUID, and $ID_FS_TYPE
    eval $(/sbin/blkid -o udev ${DEVICE})

    
    echo "Mount point: ${MNTPOINT}"

    /bin/mkdir -p ${MNTPOINT}

    # Global mount options
    OPTS="rw,relatime"

    if ! /bin/mount -o ${OPTS} ${DEVICE} ${MNTPOINT}
    then
        echo "Error mounting ${DEVICE} (status = $?)"
        /bin/rmdir ${MNTPOINT}
        exit 1
    fi

    echo "**** Mounted ${DEVICE} at ${MNTPOINT} ****"
}

do_unmount()
{
    while [[ -d $MNTPOINT ]]
    do
        if [[ -z ${MOUNTED} ]]
        then
            echo "Warning: ${DEVICE} is not mounted"
        else
            /bin/umount $MNTPOINT
            echo "**** Unmounted ${DEVICE}"
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
}

case "${ACTION}" in
    add)
        do_mount
        ;;
    remove)
        do_unmount
        ;;
    *)
        usage
        ;;
esac