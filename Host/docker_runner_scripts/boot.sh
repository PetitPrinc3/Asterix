# Runing Docker containers
/usr/bin/docker run -v USBInputDevice:/mnt/USBInputDevice:ro -v InputFiles:/mnt/InputFiles -v DataShare:/mnt/DataShare --name frontend -d -it frontend
/usr/bin/docker run -v USBOutputDevice:/mnt/USBOutputDevice -v /dev:/dev:ro -v OutputFiles:/mnt/OutputFiles:ro -v DataShare:/mnt/DataShare --name backend -d -it backend
