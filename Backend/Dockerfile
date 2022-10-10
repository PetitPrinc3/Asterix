FROM alpine:latest

# Installing software dependencies
RUN apk add python3
RUN apk add --no-cache eudev

# Installing pip
RUN python3 -m ensurepip
RUN python3 -m pip install --upgrade pip

# Adding USB Input disk handler
ADD USBHandler/* /usr/share/USBHandler/
RUN chmod +x /usr/share/USBHandler/main.py

# Adding shared libraries
ADD Asterix_libs /usr/lib/python3.10/Asterix_libs
RUN chmod 777 /usr/lib/python3.10

RUN mkdir /mnt/USBOutputDevice
RUN mkdir /dev/Backend