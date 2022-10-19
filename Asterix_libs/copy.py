import subprocess
import json
import os

from Asterix_libs.prints import *
from Asterix_libs.spinner import spinner
from Asterix_libs import hash

def copy(f1, f2):
    with spinner(f'Copying {f1} to {f2}...'):
        subprocess.call(f'/bin/cp "{f1}" "{f2}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_hash(inp_data, file):
    for d in inp_data:
        if d["FileName"] == file:
            return d["HASH"]
    return None

def xcopy(js1, f_lst, dst):
    if not os.path.isdir(dst): fail('Destination is not a directory.'); return []

    if dst[-1] != "/": dst+="/"

    try:
        with open(js1, "r") as _:
            inp_data = json.load(_)["ind_results"]
    except:
        fail('Invalid json file.')
        return []

    js_out, f = [], []

    for file in f_lst:
        
        dst_path = dst + "_".join(os.path.basename(file).split(" "))

        i = 1

        while os.path.exists(dst_path):
            dst_path = dst + ".".join(os.path.basename(file).split(".")[:-1]) + f'_{i}.' + os.path.basename(file).split(".")[-1]
            i += 1

        copy(file, dst_path)
    
        try:
            dst_hash = hash.sha(dst_path)
        except:
            dst_hash = None
    
        inp_hash = get_hash(inp_data, file)
        if inp_hash is not None: 

            if dst_hash == inp_hash:
                success(f"File {file} successfully copied to {dst_path}.")

                js_ind = {
                            "Origin": file,
                            "FileName": dst_path,
                            "HASH": dst_hash
                        }

                js_out.append(js_ind)
                f.append(dst_path)

            else:
                print (file, dst_path, inp_hash, dst_hash)
                fail(f"File copy failed.")
        
        else:
            pass
    
    with open("cp_out.json", "w") as js_cp:

        js_data = {
                    "ind_results": js_out
                }

        js_cp.seek(0)

        js_data = json.dumps(js_data, indent=4)

        js_cp.write(js_data)
        
    return f