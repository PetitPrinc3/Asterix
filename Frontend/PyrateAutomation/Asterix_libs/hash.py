#!/usr/bin/python3.10


################################################################################


# This library is not licensed


################################################################################


from hashlib import sha512


################################################################################


buffer = 65536


################################################################################


def sha(path=''):

    if path == '': return None

    hash = sha512()
    file = open(path, 'rb')

    while True:

        dat = file.read(buffer)

        if not dat :
            break

        hash.update(dat)

    return hash.hexdigest()


################################################################################


if __name__ == "__main__":
    print('Please run main.py or read software documentation')

    exit()
