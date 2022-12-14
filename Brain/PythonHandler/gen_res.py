import os
import json
import subprocess

from Asterix_libs.prints import *
from Asterix_libs.log import *

reset_log("brainRESlog.txt")

log("Generating results.", "brainRESlog.txt")

clean = json.load(open("/mnt/DataShare/clean.json", "r"))["ind_results"]
saned = json.load(open("/mnt/DataShare/san_clean.json", "r"))["ind_results"]

subprocess.call('/bin/cp default.json trt_result.json', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

with open("trt_result.json", "r+") as out:

    js_out = json.load(out)
    fls = []

    for file in clean+saned:

        subprocess.call(f'/bin/cp {file["FileName"]} /mnt/OutputFiles/{os.path.basename(file["FileName"])}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        file_ = {
            "Date": file["Date"],
            "FileName": f'/mnt/OutputFiles/{os.path.basename(file["FileName"])}',
            "HASH": file["HASH"]
        }

        fls.append(file_)

        log("Validated file : " + file_["FileName"],"brainRESlog.txt")

    js_out["ind_results"] = fls

    out.seek(0)

    js_dump = json.dumps(js_out, indent=4)

    out.write(js_dump)

subprocess.call('/bin/cp trt_result.json /mnt/DataShare/trt_result.json', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

log("End of results generation.", "brainRESlog.txt")

export_log("brainRESlog.txt")