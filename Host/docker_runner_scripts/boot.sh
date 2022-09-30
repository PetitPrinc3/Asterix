# Runing Docker containers
/usr/bin/docker run -v InputFiles:/mnt/InputFiles --name frontend -d -it frontend
/usr/bin/docker run -v /dev/bus/usb/001:/dev/bus/usb/001:ro -v OutputFiles:/mnt/OutputFiles:ro -v DataShare:/mnt/DataShare:ro --name backend -d -it backend
