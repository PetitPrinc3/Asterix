import json

# File From Hash
def ffh(json_ref, hash):

    with open(json_ref) as js_data:
        
        js = json.load(js_data)

        for file in js["ind_results"]:

            if file["HASH"] == hash:
            
                return file

    return None