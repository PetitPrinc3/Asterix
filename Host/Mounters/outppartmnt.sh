!/bin/bash

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
MNTPOINT="/var/lib/docker/volumes/USBOutputDevice/_data/USBOutputPart"

# See if this drive is already mounted, and if so where
MOUNTED=$(/bin/mount | /bin/grep ${DEVICE} | /usr/bin/awk '{ print $3 }')

do_mount()
{
    if [[ -n ${MOUNTED} ]]; then
        echo "Warning: ${DEVICE} is already mounted at ${MOUNTED}"
        exit 1
    fi

    # Get info for this drive: $ID_FS_LABEL, $ID_FS_UUID, and $ID_FS_TYPE
    eval $(/sbin/blkid -o udev ${DEVICE})

    # Figure out a mount point to use
    LABEL=${ID_FS_LABEL}
    if [[ -z "${LABEL}" ]]; then
        LABEL=${DEVBASE}
    elif /bin/grep -q " /media/${LABEL} " /etc/mtab; then
        # Already in use, make a unique one
        LABEL+="-${DEVBASE}"
    fi
    
    echo "Mount point: ${MNTPOINT}"

    /bin/mkdir -p ${MNTPOINT}

    # Global mount options
    OPTS="rw,relatime"

    # File system type specific mount options
    if [[ ${ID_FS_TYPE} == "vfat" ]]; then
        OPTS+=",users,gid=100,umask=000,shortname=mixed,utf8=1,flush"
    fi

    if ! /bin/mount -o ${OPTS} ${DEVICE} ${MNTPOINT}; then
        echo "Error mounting ${DEVICE} (status = $?)"
        /bin/rmdir ${MNTPOINT}
        exit 1
    fi

    echo "**** Mounted ${DEVICE} at ${MNTPOINT} ****"
}

do_unmount()
{
    if [[ -z ${MOUNTED} ]]; then
        echo "Warning: ${DEVICE} is not mounted"
    else
        /bin/umount -l ${DEVICE}
        echo "**** Unmounted ${DEVICE}"
    fi
    
    for f in /media/* ; do
        if [[ -n $(/usr/bin/find "$f" -maxdepth 0 -type d -empty) ]]; then
            if ! /bin/grep -q " $f " /etc/mtab; then
                echo "**** Removing mount point $f"
                /bin/rmdir "$f"
            fi
        fi
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