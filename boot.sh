# Runing Docker containers
/usr/bin/docker run --privileged -v /dev:/dev -v InputFiles:/mnt/InputFiles --name frontend -d -it frontend
/usr/bin/docker run --privileged -v /dev:/dev -v InputFiles:/mnt/InputFiles --name backend -d -it backend
