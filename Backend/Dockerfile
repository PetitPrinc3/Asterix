# Backend Dockerfile
FROM alpine:latest

# Create asterix user
RUN addgroup -S asterix && adduser -S asterix -G asterix

# Installing software dependencies
RUN apk add python3
RUN apk add --no-cache eudev

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

# Give volume permissions to user
RUN mkdir /mnt/USBOutputDevice
RUN chown -R asterix:asterix /mnt/USBOutputDevice
RUN chmod -R u=rwx /mnt/USBOutputDevice

RUN mkdir /mnt/DataShare
RUN chown -R asterix:asterix /mnt/DataShare
RUN chmod -R u=rwx /mnt/DataShare

RUN mkdir /mnt/OutputFiles
RUN chown -R asterix:asterix /mnt/OutputFiles
RUN chmod -R u=rx /mnt/OutputFiles

# Switch to Asterix user
USER asterix