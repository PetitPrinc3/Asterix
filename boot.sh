# Runing Docker containers
/usr/bin/docker run --privileged -v /dev:/dev:ro -v InputFiles:/mnt/InputFiles --name frontend -d -it frontend
/usr/bin/docker run --privileged -v /dev:/dev:ro -v InputFiles:/mnt/OutputFiles:ro --name backend -d -it backend
