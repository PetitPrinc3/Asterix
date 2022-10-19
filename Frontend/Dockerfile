# Frontend Dockerfile
FROM alpine:latest

# Create asterix user
RUN addgroup -S asterix && adduser -S asterix -G asterix

# Installing software dependencies
RUN apk add gcc
RUN apk add python3 python3-dev musl-dev
RUN apk add zlib-dev jpeg-dev
RUN apk add poppler-utils

# Installing pip
RUN python3 -m ensurepip

# Adding USB Input disk handler
ADD USBHandler/* /usr/share/USBHandler/
RUN chown -R asterix:asterix /usr/share/USBHandler
RUN chmod -R u=rwx /usr/share/USBHandler
RUN chmod -R g=rx /usr/share/USBHandler
RUN chmod -R o=-r-w-x /usr/share/USBHandler

# Adding shared libraries
ADD Asterix_libs /usr/lib/python3.10/Asterix_libs
RUN chmod -R 777 /usr/lib/python3.10/Asterix_libs

# Adding Pyrate software and multiple file processing wrapper
ADD PyrateAutomation /usr/share/PyrateAutomation
ADD PyRATE /usr/share/PyrateAutomation/Pyrate
RUN chown -R asterix:asterix /usr/share/PyrateAutomation
RUN chmod -R u=rwx /usr/share/PyrateAutomation
RUN chmod -R g=rx /usr/share/PyrateAutomation
RUN chmod -R o=-r-w-x /usr/share/PyrateAutomation

# Give volume permissions to user
RUN mkdir /mnt/USBInputDevice
RUN chown -R asterix:asterix /mnt/USBInputDevice
RUN chmod -R u=rx /mnt/USBInputDevice

RUN mkdir /mnt/InputFiles
RUN chown -R asterix:asterix /mnt/InputFiles
RUN chmod -R u=rwx /mnt/InputFiles

RUN mkdir /mnt/DataShare
RUN chown -R asterix:asterix /mnt/DataShare
RUN chmod -R u=rwx /mnt/DataShare

RUN mkdir /mnt/Sanitized
RUN chown -R asterix:asterix /mnt/Sanitized
RUN chmod -R u=rwx /mnt/Sanitized

# Switch to Asterix user
USER asterix

# Install requirements
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /usr/share/PyrateAutomation/Pyrate/requirements.txt
