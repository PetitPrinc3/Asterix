#!/usr/bin/python3.10


################################################################################


import json
import os
from Asterix_libs import hash


################################################################################


def init_json():

    ctnt = {
                'files': []
            }


    files = []


    for file in os.listdir('src'):

        f_path = f'src/{file}'
        f_name = f_path.split("/")[-1]
        f_hash = hash.sha(f_path)

        f_json = {
                'FileName': f_name,
                'FilePath': f_path,
                'HASH': f_hash
                }

        files.append(f_json)

    ctnt['files'] = files

    with open('inputs.json', 'w') as inpts:

        inpts.seek(0)

        js = json.dumps(ctnt, indent=4)

        inpts.write(js)


################################################################################


if __name__ == "__main__":
    init_json()
