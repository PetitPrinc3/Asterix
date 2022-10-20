#!/bin/bash

/usr/bin/chown root:asterix /var/lib/docker/
/usr/bin/chown root:asterix /var/lib/docker/volumes/
/usr/bin/chown root:asterix /var/lib/docker/volumes/DataShare/
/usr/bin/chown root:asterix /var/lib/docker/volumes/DataShare/_data/
/usr/bin/chmod g=rx /var/lib/docker/
/usr/bin/chmod g=rx /var/lib/docker/volumes/
/usr/bin/chmod g=rx /var/lib/docker/volumes/DataShare/
/usr/bin/chmod -R g=rx /var/lib/docker/volumes/DataShare/_data/
