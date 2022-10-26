#!/bin/bash

read -n 1 -s -r -p "Plug in USB Drives and press any key to begin."

echo BENCHMARK STARTED AT 0 SECONDS
SECONDS=0
/usr/bin/python3 /opt/asterix/Asterix.py | <<EOF
0;1;2;3;4;5;6;7;8;9;10;11;12;13
f
Y
EOF
echo BENCHMARK TERMINATED IN $SECONDS SECONDS.