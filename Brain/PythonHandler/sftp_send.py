import subprocess
import paramiko
import json
import os

from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner

target ='127.0.0.1'
username = 'ac-center'
password = 'ac-center'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

