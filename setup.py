import subprocess
from spinner import spinner
from prints import *

with spinner('Creating docker_runner user...'):
    subprocess.call("useradd -m -d /opt/docker_runner docker_runner", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success("User docker_runner created.")

with spinner('Installing Docker Engine...'):
    subprocess.call("curl -fsSL https://get.docker.com -o get-docker.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("bash get-docker.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("rm get-docker.sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
info(subprocess.call("docker version", shell=True))
success('Docker Engine installed.')

with spinner('Installing Docker Compose...'):
    subprocess.call("apt-get install libffi-dev libssl-dev", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("apt-get install libffi-dev libssl-dev", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("apt-get install -y python3 python3-pip", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("pip3 install docker-compose", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success('Docker Compose installed.')

with spinner('Enabling docker...'):
    subprocess.call("systemctl to enable Docker", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success('Docker is enabled.')

with spinner('Adding docker_runner to docker group...'):
    subprocess.call("usermod -aG docker docker_runner", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success('User docker_runner added to Docker group.')

with spinner('Creating src folder...'):
    subprocess.call("mkdir /src", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success('Folder /src created.')

with spinner('Downloading Frontend software...'):
    subprocess.call("/usr/bin/git clone https://github.com/G4vr0ch3/Frontend /src/Frontend", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("/usr/bin/chown -R docker_runner:docker /src/Frontend", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success('Frontend software downloaded.')

with spinner('Downloading Backend software...'):
    subprocess.call("/usr/bin/git clone https://github.com/G4vr0ch3/Backend /src/Backend", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("/usr/bin/chown -R docker_runner:docker /src/Backend", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success('Backend software downloaded.')

with spinner('Collecting Frontend dependencies...'):
    subprocess.call("/usr/bin/git clone https://github.com/G4vr0ch3/PyRATE /src/Frontend/PyRATE", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("/usr/bin/git clone https://github.com/G4vr0ch3/PyrateAutomation /src/Frontend/PyrateAutomation", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call("/usr/bin/git clone https://github.com/G4vr0ch3/USBInputDetection /src/Frontend/USBInputDetection", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success('Done collecting frontend dependencies.')

with spinner('Collecting Backend dependencies...'):
    subprocess.call("/usr/bin/git clone https://github.com/G4vr0ch3/USBInputDetection /src/Backend/USBInputDetection", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success('Done collecting Backend dependencies.')

with spinner('Moving files to /opt/docker_runner'):
    subprocess.call("cp docker-compose.yaml /opt/docker_runner", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
success('Done copying files to /opt/docker_runner')

with spinner('Building containers'):
    subprocess.call("docker-compose /opt/docker_runner", shell=True)
success('Done')