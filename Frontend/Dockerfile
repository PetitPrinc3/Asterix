FROM alpine:latest

# Installing software dependencies
RUN apk add gcc
RUN apk add openssh
RUN apk add python3 python3-dev musl-dev
RUN apk add zlib-dev jpeg-dev
RUN apk add poppler-utils

# Installing pip
RUN python3 -m ensurepip
RUN python3 -m pip install --upgrade pip

# Create limited user
RUN addgroup -S asterix && adduser -S asterix -G asterix

# Adding USB Input disk handler
ADD USBHandler/* /usr/share/USBHandler/
RUN chown -R asterix:asterix /usr/share/USBHandler
RUN chmod +x /usr/share/USBHandler/main.py

# Adding shared libraries
ADD Asterix_libs /usr/lib/python3.10/Asterix_libs
RUN chmod 777 /usr/lib/python3.10

# Adding Pyrate software and multiple file processing wrapper
ADD PyrateAutomation /usr/share/PyrateAutomation
ADD PyRATE /usr/share/PyrateAutomation/Pyrate
RUN chown -R asterix:asterix /usr/share/PyrateAutomation
RUN chmod +x /usr/share/PyrateAutomation/Pyrate/pyrate.py

RUN mkdir /dev/Frontend

USER asterix

RUN pip3 install -r /usr/share/PyrateAutomation/Pyrate/requirements.txt --root-user-action=ignore
