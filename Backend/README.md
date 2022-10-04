# Asterix : The Frontend

![Asterix](../Images/banner.png)

#

The Backend is one of the 4 components that make Asterix.  
Its purpose is to handle the output drive and its content :
- It checks the output drive's Vendor ID and Product ID. ✅
- It formats drives. ❌
- It copies the files chosen by the user. ✅

To better understand the role of the Backend, refer to [this](../README.md#the-project-under-construction) section.

It is presented as a Docker container and is not supposed to be installed independently from the rest of the software.

The command used to run the container is :
```bash
/usr/bin/docker run -v USBOutputDevice:/mnt/USBOutputDevice -v /dev:/dev:ro -v OutputFiles:/mnt/OutputFiles:ro -v DataShare:/mnt/DataShare --name backend -d -it backend
```
