FROM alpine:latest

# Installing software dependencies
RUN apk add openssh
RUN apk add python3 python3-dev musl-dev
RUN apk add libffi-dev gcc

# Installing pip
RUN python3 -m ensurepip
RUN python3 -m pip install --upgrade pip
RUN pip install paramiko

# Adding shared libraries
ADD Asterix_libs /usr/lib/python3.10/Asterix_libs
RUN chmod 777 /usr/lib/python3.10

# Adding Python softwares
ADD PythonHandler /usr/share/PythonHandler