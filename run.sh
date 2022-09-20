#!/bin/bash

# Input device
/usr/bin/su - docker_runner "/usr/bin/docker exec -w /usr/share/USBInputDetection -t frontend python3 main.py"
