# Runing Docker containers
/usr/bin/sudo -u docker_runner /usr/bin/docker run --privileged -v /dev:/dev -v InputFiles:/mnt/InputFiles --name frontend -d -it frontend
/usr/bin/sudo -u docker_runner /usr/bin/docker run --privileged -v /dev:/dev -v InputFiles:/mnt/InputFiles --name backend -d -it backend
