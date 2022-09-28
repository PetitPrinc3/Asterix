FROM alpine:latest

# Installing software dependencies
RUN apk add python3
RUN apk add --no-cache eudev

# Installing pip
RUN python3 -m ensurepip
RUN python3 -m pip install --upgrade pip

# Adding USB Input disk handler
ADD USBInputDetection/PythonHandler/* /usr/share/USBInputDetection/
RUN chmod +x /usr/share/USBInputDetection/main.py

RUN mkdir /mnt/USBOutputDevice
