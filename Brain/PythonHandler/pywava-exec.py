import paramiko
import sys
import os

from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner

target ='127.0.0.1'
username = 'ac-center'
password = 'ac-center'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

with spinner('Establishing connection with AC-Center...'):

    client.connect(target, port=10022, username=username, password=password)
    transport = client.get_transport()

    if transport.is_active():
        try:
            transport.send_ignore()
        except Exception as _e:
            fail('SSH Connection failed.')
            sys.exit(1)
    else:
        fail('SSH Connection failed.')
        
success('Connected to AC-Center.')


channel = transport.open_session()
c, r = os.get_terminal_size(0)
channel.get_pty(width=int(c))
channel.exec_command("cd C:\\Users\\ac-center\\Desktop\\PywavaAutomation && python main.py")
channel.shutdown_write()


while True:

    try:

        if channel.recv_ready():
            sys.stdout.write(channel.recv(4096).decode('utf-8'))

        if channel.exit_status_ready():
            sys.stdout.write(channel.recv(4096).decode('utf-8'))
            break

    except KeyboardInterrupt:
        client.close()
        fail('Operation terminated by user Keyboard Interrupt.')
   

client.close()