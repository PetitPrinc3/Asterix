#!/usr/bin/python3.10


################################################################################


import json
from Asterix_libs.log import *


################################################################################


def init_res(path):

    ctnt = {
                'ind_results': []
            }

    with open(path, "w") as results:

        log(f'Opened {path}.', "frontPYRATElog.txt")

        results.seek(0)

        js = json.dumps(ctnt, indent=4)

        results.write(js)
        log(f'Reset {path}.', "frontPYRATElog.txt")

    log(f'Closed {path}.', "frontPYRATElog.txt")


################################################################################
