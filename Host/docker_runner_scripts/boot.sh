# Runing Docker containers
/usr/bin/docker run -v USBInputDevice:/mnt/USBInputDevice:ro -v InputFiles:/mnt/InputFiles -v DataShare:/mnt/DataShare -v Sanitized:/mnt/Sanitized --name frontend -d -it frontend
/usr/bin/docker run -v USBOutputDevice:/mnt/USBOutputDevice -v /dev:/dev:ro -v OutputFiles:/mnt/OutputFiles:ro -v DataShare:/mnt/DataShare --name backend -d -it backend
/usr/bin/docker run --net=host -v InputFiles:/mnt/InputFiles -v OutputFiles:/mnt/OutputFiles -v DataShare:/mnt/DataShare -v Sanitized:/mnt/Sanitized --name brain -d -it brain
