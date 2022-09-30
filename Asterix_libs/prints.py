#!/usr/bin/python3.10


################################################################################


# A simple python library to print things beautifully.
# This library is not licensed


################################################################################


# Print green
def success(text):
    print('[+] \033[92m',text, '\033[0m')

# Print blue
def info(text):
    print('[*] \033[96m',text, '\033[0m')

# Print blue updating current row
def infor(text):
    print('[*] \033[96m',text, '\033[0m', end = '\r')

# Print orange
def warning(text):
    print('[!] \033[93m',text, '\033[0m')

# Print red
def fail(text):
    print('[-] \033[91m',text, '\033[0m')


################################################################################


if __name__ == "__main__":
    print('Please run main.py or read software documentation')
    exit()

