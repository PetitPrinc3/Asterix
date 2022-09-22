#!/bin/bash

# Input device
/usr/bin/docker exec -w /usr/share/USBInputDetection -it frontend python3 main.py
/usr/bin/docker exec -w /usr/share/USBInputDetection -it backend python3 main.py
