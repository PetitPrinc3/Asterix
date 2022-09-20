#!/bin/bash

success() {
	echo -e "$(tput setaf 2)$1$(tput sgr0)"
}

inform() {
	/usr/bin/echo -e "$(tput setaf 6)$1$(tput sgr0)"
}

warning() {
	echo -e "$(tput setaf 1)$1$(tput sgr0)"
}


inform "Creating src folder"
/usr/bin/mkdir /root/src

# Download Frontend
inform "Downloading Frontend Software"
/usr/bin/mkdir /root/src/Frontend
/usr/bin/git clone https://github.com/G4vr0ch3/Frontend /root/src/Frontend
/usr/bin/chmod +x /root/src/Frontend/setup.sh

# Download Backend
inform "Downloading Backend Software"
/usr/bin/mkdir /root/src/Backend
/usr/bin/git clone https://github.com/G4vr0ch3/Backend /root/src/Backend
/usr/bin/chmod +x /root/src/Backend/setup.sh

# Installing Frontend
inform "Installing Frontend Software"
/root/src/Frontend/setup.sh

# Installing Backend
inform "Installing Backend Software"
/root/src/Frontend/setup.sh

# Creating shared folder
inform "Creating docker shared volume"
/usr/bin/sudo -u docker_runner /usr/bin/docker volume create --name InputFiles

# Starting containers
inform "Starting containers"
/usr/bin/sudo -u docker_runner /bin/bash /opt/docker_runner/boot.sh

# SETUP END
inform "Exhausted"