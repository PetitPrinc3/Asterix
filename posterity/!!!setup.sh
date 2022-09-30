#!/bin/bash

inform() {
	/usr/bin/echo -e "$(tput setaf 6)$1$(tput sgr0)"
}

if [[$(/usr/bin/whoami) != 'root' ]]
then
	inform "The software must be run as root. Exiting"
	exit
fi

inform "Creating src folder"
/usr/bin/mkdir /src
/usr/bin/mdir /dev/Frontend
/usr/bin/mdir /dev/Backend

inform "Adding udev rules"
/usr/bin/cp 00-frontend.rules /etc/udev/rules.d
/usr/bin/cp 00-backend.rules /etc/udev/rules.d
udevadm control --reload-rules && udevadm trigger

# Download Frontend
inform "Downloading Frontend Software"
/usr/bin/git clone https://github.com/G4vr0ch3/Frontend /src/Frontend
/usr/bin/chown -R docker_runner:docker /src/Frontend
/usr/bin/chmod +x /src/Frontend/setup.sh

# Download Backend
inform "Downloading Backend Software"
/usr/bin/git clone https://github.com/G4vr0ch3/Backend /src/Backend
/usr/bin/chown -R docker_runner:docker /src/Backend
/usr/bin/chmod +x /src/Backend/setup.sh

# Installing Frontend
inform "Installing Frontend Software"
/src/Frontend/setup.sh

# Installing Backend
inform "Installing Backend Software"
/src/Backend/setup.sh

# Creating shared folders
inform "Creating docker shared volumes"
/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name InputFiles"
/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name OutputFiles"
/usr/bin/su - docker_runner -c "/usr/bin/docker volume create --name SharedDB"

inform "Creating USB UIDs database."
/usr/bin/python3 db_create.py
/usr/bin/mv USB_ID.db /var/lib/docker/volumes/SharedDB/_data

# Starting containers
inform "Starting containers"
/usr/bin/cp boot.sh /opt/docker_runner/boot.sh
/usr/bin/cp boot.sh /opt/docker_runner/run.sh
/usr/bin/su - docker_runner -c "/bin/bash /opt/docker_runner/boot.sh"

# SETUP END
inform "Exhausted"