#!/usr/bin/python3.10


################################################################################


import json


################################################################################


def get_stats(path):

    success = []
    fails = []

    with open(path, 'r') as res:

        results = json.load(res)

        for result in results['ind_results']:

            if result['SANSTat'] == True:

                success.append(result)

            else:

                fails.append(result)

    return success, fails


################################################################################
