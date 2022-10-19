FROM alpine:latest

RUN useradd asterix

# Installing software dependencies
RUN apk add gcc
RUN apk add python3 python3-dev musl-dev
RUN apk add zlib-dev jpeg-dev
RUN apk add poppler-utils

# Installing pip
RUN python3 -m ensurepip
RUN python3 -m pip install --upgrade pip

# Adding USB Input disk handler
ADD USBHandler/* /usr/share/USBHandler/
RUN chown -R asterix:asterix /usr/share/USBHandler
RUN chmod -R u=rx /usr/share/USBHandler
RUN chmod -R g=rx /usr/share/USBHandler
RUN chmod -R o=-r-w-x /usr/share/USBHandler

# Adding shared libraries
ADD Asterix_libs /usr/lib/python3.10/Asterix_libs
RUN chmod -R 777 /usr/lib/python3.10/Asterix_libs

# Adding Pyrate software and multiple file processing wrapper
ADD PyrateAutomation /usr/share/PyrateAutomation
ADD PyRATE /usr/share/PyrateAutomation/Pyrate
RUN chown -R asterix:asterix /usr/share/PyrateAutomation
RUN chmod -R u=rx /usr/share/PyrateAutomation
RUN chmod -R g=rx /usr/share/PyrateAutomation
RUN chmod -R o=-r-w-x /usr/share/PyrateAutomation

USER asterix

RUN pip3 install -r /usr/share/PyrateAutomation/Pyrate/requirements.txt --root-user-action=ignore
