# Asterix : The Frontend

![Asterix](../Images/banner.png)

#

The frontend is one of the 4 components that make Asterix.  
Its purpose is to handle the input drive and its content :
- It lists the drives content.
- It copies the files chosen by the user.
- It sanitizes the infected files selected by the user.

To better understand the role of the Frontend, refer to [this](../README.md#the-project-under-construction) section.

It is presented as a Docker container and is not supposed to be installed independently from the rest of the software.

The command used to run the container is :
```bash
/usr/bin/docker run -v USBInputDevice:/mnt/USBInputDevice:ro -v InputFiles:/mnt/InputFiles -v DataShare:/mnt/DataShare --name frontend -d -it frontend
```
