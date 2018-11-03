from flask import json

def price(dishName):
    fake = {
        'CourseID': 1,
        'Price': 20
    }
    print("do something")
    return json.dumps(fake)
