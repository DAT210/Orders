import json

# takes a string with a file name, returns a single dict with all the data

def json_to_dict(filename):
    with open(filename) as dummy:
        data = json.load(dummy)
    
    type_key = list(data.keys())[0]
    return data[type_key]
