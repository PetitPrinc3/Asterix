#!/usr/bin/python3.10


################################################################################


import os.path
import json
import hash


################################################################################


def lst(pathfile):
    fls=[]
    for path, dirs, files in os.walk(pathfile):
        for filename in files:
            fls.append(path + "/" + filename)

    for i in range(len(fls)):

        path = fls[i]
        if os.path.isfile(path):
            a=hash.sha(path)
            with open ("list_result.json", 'r+') as results:
                f_data = json.load(results)
                ind_result={
                    "FileName":fls[i],
                    "HASH":a,
                }
                f_data["ind_results"].append(ind_result)
                results.seek(0)
                js = json.dumps(f_data,indent=4)
                results.write(js)
    return fls


################################################################################