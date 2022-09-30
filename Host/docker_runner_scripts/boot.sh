# Runing Docker containers
/usr/bin/docker run --privileged -v /dev/Frontend:/dev/Frontend:ro -v InputFiles:/mnt/InputFiles --name frontend -d -it frontend
/usr/bin/docker run --privileged -v /dev/Backend:/dev/Backend:ro -v OutputFiles:/mnt/OutputFiles:ro -v SharedDB:/mnt/SharedDB:ro --name backend -d -it backend
