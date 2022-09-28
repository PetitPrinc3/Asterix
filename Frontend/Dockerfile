FROM alpine:latest

# Installing software dependencies
RUN apk add gcc
RUN apk add python3 python3-dev musl-dev
RUN apk add zlib-dev jpeg-dev
RUN apk add poppler-utils

# Installing pip
RUN python3 -m ensurepip
RUN python3 -m pip install --upgrade pip

# Adding USB Input disk handler
ADD USBInputDetection/* /usr/share/USBInputDetection/
RUN chmod +x /usr/share/USBInputDetection/main.py
RUN mkdir /mnt/USBInputDevice

# Adding Pyrate software and multiple file processing wrapper
ADD PyrateAutomation /usr/share/PyrateAutomation
ADD PyRATE /usr/share/PyrateAutomation/Pyrate
RUN chmod +x /usr/share/PyrateAutomation/Pyrate/pyrate.py
RUN pip3 install -r /usr/share/PyrateAutomation/Pyrate/requirements.txt --root-user-action=ignore

RUN mkdir /dev/Frontend