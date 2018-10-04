import json
from werkzeug.security import generate_password_hash

# takes a string with a file name, returns a list of dicts dict with all the data and 
# a string describing where it is coming to/from (e.g. "Orders", "Customers", "Delivery")
def json_to_dict(filename):
    with open(filename) as dummy:
        data = json.loads(dummy.read())
    if len(data) == 1:
        type_key = list(data.keys())[0]
        return (data[type_key], type_key)
    else:
        return(data, "Probably menu...")
        
def salt_it(password):
    salty_password = generate_password_hash(password)
    return salty_password

# whatever - data you want in your json, target - a string describing where 
# it is coming to/from (e.g. "Orders", "Customers", "Delivery")
def whatever_to_json(whatever, target, filename):
    for item in whatever:
        if type(item) is dict:
            for key in item:
                if str(key).lower() == "password":
                    item[key] = salt_it(item[key])
                        
    ready_to_dump= {}
    ready_to_dump[target] = whatever
    with open(filename, 'w') as target_file:
        json.dump(ready_to_dump, target_file)


