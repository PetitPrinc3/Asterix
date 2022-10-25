#!/bin/bash

/usr/bin/cp /opt/asterix/.config/pcmanfm/LXDE-pi/pcmanfm.conf /opt/asterix/.config/pcmanfm/LXDE-pi/pcmanfm.conf.backup
/usr/bin/sed -i.backup 's/mount_on_startup=.*/mount_on_startup=0/' /opt/asterix/.config/pcmanfm/LXDE-pi/pcmanfm.conf
/usr/bin/sed -i 's/mount_removable=.*/mount_removable=0/' /opt/asterix/.config/pcmanfm/LXDE-pi/pcmanfm.conf
