#!/bin/bash

# Input device
/usr/bin/docker exec -w /usr/share/USBInputDetection -it -d frontend python3 main.py
/usr/bin/docker exec -w /usr/share/USBInputDetection -it -d backend python3 main.py
