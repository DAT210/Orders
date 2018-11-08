from flask import json


def availability(date):
    # todo send fake json about availability on specified date
    print("do something")


def price(dishName):
    # todo change into sending json for specified dish
    dict = getList()
    if dict['c_name'] == dishName:
        return json.dumps(dict)


def getList():
    with open("static/fakePrice.json", "r") as f:
        print(f)
        return json.load(f)
