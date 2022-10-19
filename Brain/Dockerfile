# Brain Dockerfile
FROM alpine:latest

# Create asterix user
RUN addgroup -S asterix && adduser -S asterix -G asterix

# Installing software dependencies
RUN apk add openssh
RUN apk add python3 python3-dev musl-dev
RUN apk add libffi-dev gcc

# Installing pip
RUN python3 -m ensurepip

# Adding shared libraries
ADD Asterix_libs /usr/lib/python3.10/Asterix_libs
RUN chmod -R 777 /usr/lib/python3.10/Asterix_libs

# Adding Python softwares
ADD PythonHandler /usr/share/PythonHandler
RUN chown -R asterix:asterix /usr/share/PythonHandler
RUN chmod -R u=rwx /usr/share/PythonHandler
RUN chmod -R g=rx /usr/share/PythonHandler
RUN chmod -R o=-r-w-x /usr/share/PythonHandler

# Give volume permissions to user
RUN mkdir /mnt/InputFiles
RUN chown -R asterix:asterix /mnt/InputFiles
RUN chmod -R u=rwx /mnt/InputFiles

RUN mkdir /mnt/OutputFiles
RUN chown -R asterix:asterix /mnt/OutputFiles
RUN chmod -R u=rx /mnt/OutputFiles

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
RUN pip3 install paramiko