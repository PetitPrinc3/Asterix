#!/usr/bin/python3.10


################################################################################


import os
import json
import paramiko
from Asterix_libs import log


################################################################################


def init_res(channel, path):

    fname = os.path.basename(path)

    ctnt = {
                'ind_results': []
            }

    with open(fname, "w") as results:

        results.seek(0)

        js = json.dumps(ctnt, indent=4)

        results.write(js)

    print(fname, path, channel.put(fname, path))


################################################################################
