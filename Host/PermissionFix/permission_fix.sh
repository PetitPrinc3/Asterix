#!/bin/bash

/usr/bin/cp Host/Asterix.py /opt/asterix/Asterix.py
/usr/bin/chown -R asterix:asterix /opt/asterix
/usr/bin/chmod -R u=rwx /opt/asterix
/usr/bin/chmod -R g=rwx /opt/asterix
/usr/bin/chmod -R o=-r-w-x /opt/asterix
/usr/bin/chown -R docker_runner:docker_runner /opt/docker_runner
/usr/bin/chmod -R u=rwx /opt/docker_runner
/usr/bin/chmod -R g=rwx /opt/docker_runner
/usr/bin/chmod -R o=-r-w-x /opt/docker_runner
/usr/bin/chown root:asterix /var/lib/docker/
/usr/bin/chown root:asterix /var/lib/docker/volumes/
/usr/bin/chown root:asterix /var/lib/docker/volumes/DataShare/
/usr/bin/chown root:asterix /var/lib/docker/volumes/DataShare/_data/
/usr/bin/chmod g=rx /var/lib/docker/
/usr/bin/chmod g=rx /var/lib/docker/volumes/
/usr/bin/chmod g=rx /var/lib/docker/volumes/DataShare/
/usr/bin/chmod -R g=rx /var/lib/docker/volumes/DataShare/_data/
