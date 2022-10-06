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
    client.open_sftp()
        
success('Connected to AC-Center.')

