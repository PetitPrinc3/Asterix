#!/usr/bin/python3.10


################################################################################


import json
from Asterix_libs import log


################################################################################


def init_res(path):

    ctnt = {
                'ind_results': []
            }

    with open(path, "w") as results:

        log.log(f'Opened {path}.')

        results.seek(0)

        js = json.dumps(ctnt, indent=4)

        results.write(js)
        log.log(f'Reset {path}.')

    log.log(f'Closed {path}.')


################################################################################
