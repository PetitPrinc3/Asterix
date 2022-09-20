#!/bin/bash

inform() {
	/usr/bin/echo -e "$(tput setaf 6)$1$(tput sgr0)"
}

inform "Creating src folder"
/usr/bin/mkdir /src

# Download Frontend
inform "Downloading Frontend Software"
/usr/bin/git clone https://github.com/G4vr0ch3/Frontend /src/Frontend
/usr/bin/chmod +x /src/Frontend/setup.sh

# Download Backend
inform "Downloading Backend Software"
/usr/bin/git clone https://github.com/G4vr0ch3/Backend /src/Backend
/usr/bin/chmod +x /src/Backend/setup.sh

# Installing Frontend
inform "Installing Frontend Software"
/src/Frontend/setup.sh

# Installing Backend
inform "Installing Backend Software"
/src/Backend/setup.sh

# Creating shared folder
inform "Creating docker shared volume"
/usr/bin/su - docker_runner "/usr/bin/docker volume create --name InputFiles"

# Starting containers
inform "Starting containers"
/usr/bin/cp boot.sh /opt/docker_runner/boot.sh
/usr/bin/cp boot.sh /opt/docker_runner/run.sh
/usr/bin/su - docker_runner "/bin/bash /opt/docker_runner/boot.sh"

# SETUP END
inform "Exhausted"