#!/bin/bash

# This script is called from our systemd unit file to mount a USB drive.

DEVBASE=$1
DEVICE="/dev/${DEVBASE}"
MNTBASE="/var/lib/docker/volumes/USBInputDevice/_data/USBInputPart/"
MNTPOINT=$MNTBASE$DEVBASE

# See if this drive is already mounted, and if so where
MOUNTED=$(/bin/mount | /bin/grep ${DEVICE} | /usr/bin/awk '{ print $3 }')

if [[ -n ${MOUNTED} ]]
then
    echo "Warning: ${DEVICE} is already mounted at ${MOUNTED}"
    exit 1
fi

# Get info for this drive: $ID_FS_LABEL, $ID_FS_UUID, and $ID_FS_TYPE
eval $(/sbin/blkid -o udev ${DEVICE})


echo "Mount point: ${MNTPOINT}"

/bin/mkdir -p $MNTPOINT

# Global mount options
OPTS="ro,relatime"

if ! /bin/mount -o $OPTS $DEVICE $MNTPOINT
then
    echo "Error mounting ${DEVICE} (status = $?)"
    /bin/rmdir $MNTPOINT
    exit 1
fi

echo "**** Mounted ${DEVICE} at ${MNTPOINT} ****"
